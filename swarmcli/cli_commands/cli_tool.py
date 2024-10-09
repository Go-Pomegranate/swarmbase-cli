
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
def tool(ctx):
    """Commands for managing tools"""


@tool.command()
@click.option("--name", required=True, help="Name of the tool")
@click.option("--description", help="Description of the tool")
@click.option("--version", help="Name of the tool")
@click.option("--code", help="Code of the tool")
@click.option(
    "--extra_attributes",
    help="Extra attributes of the tool specified in a dictionary",
)
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def create(ctx, name, description, version, code, extra_attributes):
    """Create a new tool"""
    logger = ctx.obj["logger"]
    logger.debug(
        f"Creating tool with name: {name}, description: {description}, version: {version}, code: {code}, extra_attributes: {extra_attributes},",
    )

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    tool = swarm_cli.create_tool(
        name,
        description,
        version,
        code,
        extra_attributes,
    )
    click.echo(tool)


@tool.command()
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def list(ctx):
    """List all tools"""
    logger = ctx.obj["logger"]
    logger.debug("Listing all tools")

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    tools = swarm_cli.list_tools()
    click.echo(tools)


@tool.command()
@click.argument("tool_id")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def get(ctx, tool_id):
    """Get a tool by ID"""
    logger = ctx.obj["logger"]
    logger.debug(f"Getting tool with ID: {tool_id}")

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    tool = swarm_cli.get_tool(tool_id)
    click.echo(tool)


@tool.command()
@click.argument("tool_id")
@click.option("--name", required=True, help="New name of the tool")
@click.option("--description", help="New description of the tool")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def update(ctx, tool_id, name, description):
    """Update a tool"""
    logger = ctx.obj["logger"]
    logger.debug(
        f"Updating tool with ID: {tool_id}, name: {name}, description: {description}",
    )

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    tool = swarm_cli.update_tool(tool_id, name, description)
    click.echo(tool)


@tool.command()
@click.argument("tool_id")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def delete(ctx, tool_id):
    """Delete a tool"""
    logger = ctx.obj["logger"]
    logger.debug(f"Deleting tool with ID: {tool_id}")

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    response = swarm_cli.delete_tool(tool_id)
    click.echo(response)
