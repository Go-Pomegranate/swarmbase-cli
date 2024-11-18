"""Utlis for SwarmCLI."""

import json
import logging
from enum import Enum
from functools import wraps
from json import JSONDecodeError
from pathlib import Path
from re import sub
from typing import NamedTuple
import requests
import click
from swarmcli.version import __version__

CONFIG_FILE = Path.expanduser(Path("~/.swarm_cli_config.json"))


def load_config():
    if Path(CONFIG_FILE).is_file():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}


def save_config(config) -> None:
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)


def setup_logging(debug: bool):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    return logger


@click.group(invoke_without_command=True)
@click.option("--base-url", help="Base URL of the swarmbase.ai API")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@click.version_option(
    version=__version__, prog_name="Swarmbase CLI", message="%(prog)s %(version)s"
)
def cli(ctx: click.Context, base_url: str, debug: bool) -> None:
    config = load_config()
    if base_url:
        config["base_url"] = base_url
        save_config(config)
    elif "base_url" not in config:
        click.echo("Error: --base-url is required for the first use.")
        ctx.exit(1)

    ctx.obj = config
    ctx.obj["logger"] = setup_logging(debug)
    ctx.obj["logger"].debug("Debugging enabled")

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


def debug_logging(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ctx = click.get_current_context()
        logger = ctx.obj["logger"]
        debug = kwargs.pop("debug", False)
        if debug:
            logger.setLevel(logging.DEBUG)
            logger.debug("Debugging enabled")
        return func(*args, **kwargs)

    return wrapper


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ctx = click.get_current_context()
        logger = ctx.obj["logger"]
        try:
            return func(*args, **kwargs)
        except requests.exceptions.MissingSchema:
            logger.exception(
                "Invalid URL. Make sure the URL starts with http:// or https://.",
            )
            click.echo(
                "Error: Invalid URL. Make sure the URL starts with http:// or https://.",
            )
        except requests.exceptions.ConnectionError:
            logger.exception("Network connection error occurred.")
            click.echo("Error: Network connection error occurred.")
        except requests.exceptions.Timeout:
            logger.exception("Request timed out.")
            click.echo("Error: Request timed out.")
        except requests.exceptions.HTTPError as http_err:
            logger.exception("HTTP error occurred: ")
            click.echo(f"Error: HTTP error occurred: {http_err}")
        except KeyError:
            logger.exception("SwarmCLI base URL not found in context object.")
            click.echo("Error: SwarmCLI base URL not found in context object.")
        except JSONDecodeError as json_decode_err:
            logger.exception("Failed to parse JSON data.")
            click.echo(
                f"Invalid JSON format. Please check the input data.\
                    Error: {json_decode_err}",
            )
        except Exception as e:
            logger.exception("An unexpected error occurred")
            click.echo(f"An unexpected error occurred: {e}")

    return wrapper


class RelationshipType(str, Enum):
    COLLABORATES = "collaborates"
    SUPERVISES = "supervises"


class AgentRelationship(NamedTuple):
    relationship_type: RelationshipType
    source_agent_id: str
    target_agent_id: str


# https://stackoverflow.com/questions/44247099/click-command-line-interfaces-make-options-required-if-other-optional-option-is
class Mutex(click.Option):
    def __init__(self, *args, **kwargs) -> None:
        self.not_required_if: list = kwargs.pop("not_required_if")

        assert self.not_required_if, "'not_required_if' parameter required"
        kwargs["help"] = (
            kwargs.get("help", "")
            + "Option is mutually exclusive with "
            + ", ".join(self.not_required_if)
            + "."
        ).strip()
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx: click.Context, opts, args):
        current_opt: bool = self.name in opts
        for mutex_opt in self.not_required_if:
            if mutex_opt in opts:
                if current_opt:
                    raise click.UsageError(
                        "Illegal usage: '"
                        + str(self.name)
                        + "' is mutually exclusive with "
                        + str(mutex_opt)
                        + ".",
                    )
                self.prompt = None
        return super().handle_parse_result(ctx, opts, args)


def pascal_case(s):
    return sub(r"(_|-| )+", " ", s).title().replace(" ", "")


def snake_case(s):
    return "_".join(
        sub(
            "([A-Z][a-z]+)",
            r" \1",
            sub("([A-Z]+)", r" \1", s.replace("-", " ")),
        ).split(),
    ).lower()
