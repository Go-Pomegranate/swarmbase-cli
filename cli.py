"""SwarmCLI entry point."""

from swarmcli import cli_commands  # noqa: F401
from swarmcli.utils import (
    cli,
)

if __name__ == "__main__":
    cli(obj={})
