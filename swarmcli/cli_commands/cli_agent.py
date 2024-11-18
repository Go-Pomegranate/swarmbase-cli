import click

from swarmcli.facade import SwarmCLI
from swarmcli.utils import (
    Mutex,
    RelationshipType,
    cli,
    debug_logging,
    handle_exceptions,
)


@cli.group()
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
def agent(ctx) -> None:
    """Commands for managing agents"""


@agent.command()
@click.option("--name", required=True, help="Name of the agent")
@click.option("--description", help="Description of the agent")
@click.option("--instructions", help="Instructions for the agent")
@click.option(
    "--extra_attributes", help="Extra attributes of the agent specified in a dictionary"
)
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def create(ctx, name, description, instructions, extra_attributes) -> None:
    """Create a new agent"""
    logger = ctx.obj["logger"]
    logger.debug(
        f"Creating agent with name: {name}\
              description: {description},\
                  instructions: {instructions},\
                    extra_attributes: {extra_attributes}",
    )

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    agent = swarm_cli.create_agent(name, description, instructions, extra_attributes)
    click.echo(agent)


@agent.command()
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def list(ctx) -> None:
    """List all agents"""
    logger = ctx.obj["logger"]
    logger.debug("Listing all agents")

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    agents = swarm_cli.list_agents()
    click.echo(agents)


@agent.command()
@click.argument("agent_id")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def get(ctx, agent_id) -> None:
    """Get an agent by ID"""
    logger = ctx.obj["logger"]
    logger.debug(f"Getting agent with ID: {agent_id}")

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    agent = swarm_cli.get_agent(agent_id)
    click.echo(agent)


@agent.command()
@click.argument("agent_id")
@click.option("--name", required=True, help="New name of the agent")
@click.option("--description", help="New description of the agent")
@click.option("--instructions", help="Instructions for the agent")
@click.option(
    "--extra_attributes", help="Extra attributes of the agent specified in a dictionary"
)
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def update(ctx, agent_id, name, description, instructions, extra_attributes) -> None:
    """Update an agent"""
    logger = ctx.obj["logger"]
    logger.debug(
        f"Updating agent with ID: {agent_id}, name: {name}, description: {description}, instructions: {instructions}, extra_attributes: {extra_attributes}.",
    )

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    agent = swarm_cli.update_agent(
        agent_id, name, description, instructions, extra_attributes
    )
    click.echo(agent)


@agent.command()
@click.argument("agent_id")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def delete(ctx, agent_id) -> None:
    """Delete an agent"""
    logger = ctx.obj["logger"]
    logger.debug(f"Deleting agent with ID: {agent_id}")

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    response = swarm_cli.delete_agent(agent_id)
    click.echo(response)


@agent.command()
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.option("--agent1", required=True, help="Id of the first agent")
@click.option("--agent2", required=True, help="Id of the second agent")
@click.option(
    "--relationship",
    type=click.Choice(RelationshipType),
    help="Relationship betwen the agents",
)
@click.pass_context
@debug_logging
@handle_exceptions
def link(ctx, agent1, agent2, relationship) -> None:
    """Establish a relationship between two existing agents."""
    agent_id = agent1
    related_agent_id = agent2
    relationship_type = RelationshipType(relationship)
    logger = ctx.obj["logger"]
    logger.debug(
        f"Linking primary agent {agent_id} and related agent {related_agent_id} with relationship: {relationship_type}",
    )

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    response = swarm_cli.add_agent_relationship(
        agent_id,
        related_agent_id,
        relationship_type,
    )
    click.echo(response)


@agent.command()
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.option("--agent1", required=True, help="Id of the first agent")
@click.option("--agent2", required=True, help="Id of the second agent")
@click.pass_context
@debug_logging
@handle_exceptions
def unlink(ctx, agent1, agent2) -> None:
    """Remove a relationship between two existing agents."""
    agent_id = agent1
    related_agent_id = agent2
    logger = ctx.obj["logger"]
    logger.debug(
        f"Unlinking primary agent {agent_id} and related agent {related_agent_id}",
    )

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    response = swarm_cli.remove_agent_relationship(agent_id, related_agent_id)
    click.echo(response)


@agent.command()
@click.argument("agent_id")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def get_relationships(ctx, agent_id) -> None:
    """Get an agent's relationships"""
    logger = ctx.obj["logger"]
    logger.debug(f"Getting agent relationships with ID: {agent_id}")

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    agent = swarm_cli.get_agent_relationships(agent_id)
    click.echo(agent)


@agent.command()
@click.argument("agent_id")
@click.option(
    "--tool_id",
    required=False,
    cls=Mutex,
    help="Id of the tool",
    not_required_if=["name", "description"],
)
@click.option(
    "--name",
    cls=Mutex,
    not_required_if=["tool"],
    help="Name of the tool",
)
@click.option(
    "--description",
    cls=Mutex,
    not_required_if=["tool"],
    help="Description of the tool",
)
@click.option("--version", help="Version of the tool")
@click.option("--code", help="Code of the tool")
@click.option(
    "--extra_attributes",
    required=False,
    help="Extra attributes of the tool specified in a dictionary",
)
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def add_tool(
    ctx,
    agent_id,
    tool_id,
    name,
    description,
    version,
    code,
    extra_attributes,
) -> None:
    """Adds tool to an agent. Specify tool id if tool is added by id"""
    logger = ctx.obj["logger"]

    if tool_id:
        logger.debug(f"Adding tool {tool_id} to the agent {agent_id}")
        tool_data = {"tool_id": tool_id}

    else:
        f"Adding tool with name: {name}, description: {description}, version: {version}, code: {code}, extra_attributes: {extra_attributes} to the agent {agent_id}"

        logger.debug(f"Adding tool {tool_id} to the agent {agent_id}")

        tool_data = {
            "name": name,
            "description": description,
            "version": version,
            "code": code,
            "extra_attributes": extra_attributes,
        }

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    response = swarm_cli.assign_tool_to_agent(agent_id, tool_data)
    click.echo(response)


@agent.command()
@click.argument("agent_id")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.option(
    "--tool_id",
    required=True,
    help="Id of the tool to be removed from an agent",
)
@click.pass_context
@debug_logging
@handle_exceptions
def remove_tool(ctx, agent_id, tool_id) -> None:
    """Removes tool from an agents."""
    logger = ctx.obj["logger"]
    logger.debug(f"Unlinking tool {tool_id} from the agent {agent_id}")

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    response = swarm_cli.remove_tool_from_agent(agent_id, tool_id)
    click.echo(response)


@agent.command()
@click.argument("agent_id")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def get_tools(ctx, agent_id) -> None:
    """Get an agent's relationships"""
    logger = ctx.obj["logger"]
    logger.debug(f"Getting agent tools with ID: {agent_id}")

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    agent = swarm_cli.get_agent_tools(agent_id)
    click.echo(agent)
