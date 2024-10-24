import click

from swarmcli.facade import SwarmCLI
from swarmcli.utils import (
    Mutex,
    cli,
    debug_logging,
    handle_exceptions,
)


@cli.group()
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def swarm(ctx):
    """Commands for managing swarms"""


@swarm.command()
@click.option("--name", required=True, help="Name of the swarm")
@click.option("--extra_attributes", help="Extra attributes of the swarm")
@click.option("--parent_id", help="Swarm's parent id")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def create(ctx, name, parent_id, extra_attributes):
    """Create a new swarm"""
    logger = ctx.obj["logger"]
    logger.debug(
        f"Creating swarm with name: {name},  parent_id: {parent_id}, extra_attributes: {extra_attributes}",
    )

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    swarm = swarm_cli.create_swarm(name, parent_id, extra_attributes)
    click.echo(swarm)


@swarm.command()
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def list(ctx):
    """List all swarms"""
    logger = ctx.obj["logger"]
    logger.debug("Listing all swarms")

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    swarms = swarm_cli.list_swarms()
    click.echo(swarms)


@swarm.command()
@click.argument("swarm_id")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def get(ctx, swarm_id):
    """Get a swarm by ID"""
    logger = ctx.obj["logger"]
    logger.debug(f"Getting swarm with ID: {swarm_id}")

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    swarm = swarm_cli.get_swarm(swarm_id)
    click.echo(swarm)


@swarm.command()
@click.argument("swarm_id")
@click.option("--name", required=True, help="New name of the swarm")
@click.option("--description", help="New description of the swarm")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def update(ctx, swarm_id, name, description):
    """Update a swarm"""
    logger = ctx.obj["logger"]
    logger.debug(
        f"Updating swarm with ID: {swarm_id}, name: {name}, description: {description}",
    )

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    swarm = swarm_cli.update_swarm(swarm_id, name, description)
    click.echo(swarm)


@swarm.command()
@click.argument("swarm_id")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def delete(ctx, swarm_id):
    """Delete a swarm"""
    logger = ctx.obj["logger"]
    logger.debug(f"Deleting swarm with ID: {swarm_id}")

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    response = swarm_cli.delete_swarm(swarm_id)
    click.echo(response)


@swarm.command()
@click.option(
    "--swarm_id",
    help="Id of the swarm",
    required=True,
)
@click.option(
    "--agent_id",
    required=True,
    help="Id of the agent",
)
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def add_agent(
    ctx,
    swarm_id,
    agent_id,
) -> None:
    """Adds agent to the swarm. Specify agent id"""
    logger = ctx.obj["logger"]

    if agent_id:
        logger.debug(f"Adding agent {agent_id} to the swarm {swarm_id}")
        agent_data = {"agent_id": agent_id}

    # TODO add handling if agent_id is not provided?

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    response = swarm_cli.add_agent_to_swarm(swarm_id, agent_data)
    click.echo(response)


@swarm.command()
@click.option(
    "--swarm_id",
    help="Id of the swarm",
    required=True,
)
@click.option(
    "--agent_id",
    required=True,
    help="Id of the agent",
)
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def remove_agent(
    ctx,
    swarm_id,
    agent_id,
) -> None:
    """Removes agent from the swarm. Specify agent id"""
    logger = ctx.obj["logger"]

    if agent_id:
        logger.debug(f"Removing agent {agent_id} from the swarm {swarm_id}")
        agent_data = {"agent_id": agent_id}

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    response = swarm_cli.remove_agent_from_swarm(swarm_id, agent_data)
    click.echo(response)


@swarm.command()
@click.argument("swarm_id")
@click.option("--framework_name", help="Name of the framework", required=False)
@click.option("--base_path", required=False)
@click.option("--requirements_file", required=False)
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def export(ctx, swarm_id, framework_name, base_path, requirements_file):
    """Export swarm"""
    logger = ctx.obj["logger"]
    logger.debug(f"Exporting swarm with ID: {swarm_id}")

    if framework_name is None:
        framework_name = "swarmbasecore"
    data = {
        "swarm_id": swarm_id,
        "framework_name": framework_name,
        "base_path": base_path,
        "requirements_file": requirements_file,
    }

    data = {k: v for k, v in data.items() if v is not None}

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    response = swarm_cli.export_swarm(**data)
    click.echo(response)
