
import click

from swarmcli.facade import SwarmCLI
from swarmcli.utils import (
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
