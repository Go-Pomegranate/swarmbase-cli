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
@click.option("--version", help="Version of the tool")
@click.option("--code", help="Code of the tool")
@click.option(
    "--inputs",
    help="Inputs of the tool. Example: {'name': 'first_param', 'type':'str', 'description': 'the first parameter of the funciton'}",
)
@click.option(
    "--outputs",
    help="Outputs of the tool. Example: {'name': 'output', 'type':'str', 'description': 'the output of the funciton'}",
)
@click.option(
    "--extra_attributes",
    help="Extra attributes of the tool specified in a dictionary",
)
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def create(ctx, name, description, version, code, inputs, outputs, extra_attributes):
    """Create a new tool"""
    logger = ctx.obj["logger"]
    logger.debug(
        f"Creating tool with name: {name}, description: {description}, version: {version}, code: {code}, inputs: {inputs}, outputs: {outputs}, extra_attributes: {extra_attributes},",
    )

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    tool = swarm_cli.create_tool(
        name,
        description,
        version,
        code,
        inputs,
        outputs,
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
@click.option("--tool_id", "--id")
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
@click.option("--tool_id", "--id")
@click.option("--name", required=False, help="New name of the tool")
@click.option("--description", help="New description of the tool")
@click.option("--code", help="New code of the tool")
@click.option("--inputs", help="New inputs of the tool")
@click.option("--outputs", help="New outputs of the tool")
@click.option("--version", help="New version of the tool")
@click.option("--extra_attributes", help="New extra attributes of the tool")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def update(
    ctx,
    tool_id,
    name,
    description,
    code,
    inputs,
    outputs,
    version,
    extra_attributes,
):
    """Update a tool"""
    logger = ctx.obj["logger"]
    logger.debug(
        f"Updating tool with ID: {tool_id}, name: {name}, description: {description}, code: {code}, inputs: {inputs}, outputs: {outputs}, version: {version}, extra_attributes: {extra_attributes}",
    )

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    update_data = {
        "tool_id": tool_id,
        "name": name,
        "description": description,
        "code": code,
        "inputs": inputs,
        "outputs": outputs,
        "version": version,
        "extra_attributes": extra_attributes,
    }
    update_data = {k: v for k, v in update_data.items() if v is not None}
    tool = swarm_cli.update_tool(**update_data)
    click.echo(tool)


@tool.command()
@click.option("--tool_id", "--id")
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
