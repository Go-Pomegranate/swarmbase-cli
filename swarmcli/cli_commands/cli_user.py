"""Click commands for user management."""

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
def user(ctx):
    """Commands for managing users"""


@user.command()
@click.option("--name", required=True, help="Name of the user")
@click.option("--email", required=True, help="Email of the user")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def create(ctx, name, email):
    """Create a new user"""
    logger = ctx.obj["logger"]
    logger.debug(f"Creating user with name: {name}, email: {email}")

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    user = swarm_cli.create_user(name, email)
    click.echo(user)


@user.command()
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def list(ctx):
    """List all users"""
    logger = ctx.obj["logger"]
    logger.debug("Listing all users")

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    users = swarm_cli.list_users()
    click.echo(users)


@user.command()
@click.argument("user_id")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def get(ctx, user_id):
    """Get a user by ID"""
    logger = ctx.obj["logger"]
    logger.debug(f"Getting user with ID: {user_id}")

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    user = swarm_cli.get_user(user_id)
    click.echo(user)


@user.command()
@click.argument("user_id")
@click.option("--name", required=True, help="New name of the user")
@click.option("--email", required=True, help="New email of the user")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def update(ctx, user_id, name, email):
    """Update a user"""
    logger = ctx.obj["logger"]
    logger.debug(
        f"Updating user with ID: {user_id}, name: {name}, email: {email}",
    )

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    user = swarm_cli.update_user(user_id, name, email)
    click.echo(user)


@user.command()
@click.argument("user_id")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def delete(ctx, user_id):
    """Delete a user"""
    logger = ctx.obj["logger"]
    logger.debug(f"Deleting user with ID: {user_id}")

    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    response = swarm_cli.delete_user(user_id)
    click.echo(response)
