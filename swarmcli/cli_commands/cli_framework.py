
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
def framework(ctx):
    """Commands for managing frameworks"""


@framework.command()
@click.option("--name", required=True, help="Name of the framework")
@click.option("--description", help="Description of the framework")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def create(ctx, name, description):
    """Create a new framework"""
    logger = ctx.obj["logger"]
    logger.debug(
        f"Creating framework with name: {name}, description: {description}",
    )

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    framework = swarm_cli.create_framework(name, description)
    click.echo(framework)


@framework.command()
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def list(ctx):
    """List all frameworks"""
    logger = ctx.obj["logger"]
    logger.debug("Listing all frameworks")

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    frameworks = swarm_cli.list_frameworks()
    click.echo(frameworks)


@framework.command()
@click.argument("framework_id")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def get(ctx, framework_id):
    """Get a framework by ID"""
    logger = ctx.obj["logger"]
    logger.debug(f"Getting framework with ID: {framework_id}")

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    framework = swarm_cli.get_framework(framework_id)
    click.echo(framework)


@framework.command()
@click.argument("framework_id")
@click.option("--name", required=True, help="New name of the framework")
@click.option("--description", help="New description of the framework")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def update(ctx, framework_id, name, description):
    """Update a framework"""
    logger = ctx.obj["logger"]
    logger.debug(
        f"Updating framework with ID: {framework_id}, name: {name}, description: {description}",
    )

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    framework = swarm_cli.update_framework(framework_id, name, description)
    click.echo(framework)


@framework.command()
@click.argument("framework_id")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def delete(ctx, framework_id):
    """Delete a framework"""
    logger = ctx.obj["logger"]
    logger.debug(f"Deleting framework with ID: {framework_id}")

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    response = swarm_cli.delete_framework(framework_id)
    click.echo(response)


@framework.command()
@click.argument("framework_id")
@click.option("--swarm_id", required=True, help="ID of the swarm")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def add_swarm(ctx, framework_id, swarm_id):
    """Add swarm to framework"""
    logger = ctx.obj["logger"]
    logger.debug(f"Adding swarm to framework with ID: {framework_id}")

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    relationship = swarm_cli.assign_swarm_to_framework(framework_id, swarm_id)
    click.echo(relationship)


@framework.command()
@click.argument("framework_id")
@click.option("--swarm_id", required=True, help="ID of the swarm")
@click.option("--swarm_name", required=True, help="Name of the swarm")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def remove_swarm(ctx, framework_id, swarm_id):
    """Add swarm to framework"""
    logger = ctx.obj["logger"]
    logger.debug(f"Adding swarm to framework with ID: {framework_id}")

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    relationship = swarm_cli.assign_swarm_to_framework(framework_id, swarm_id)
    click.echo(relationship)
