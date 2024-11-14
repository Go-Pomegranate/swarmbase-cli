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
def migrator(ctx):
    """Commands for managing migrations"""

@migrator.command()
@click.option('--source', required=True, help='Path to the source data.')
@click.option('--destination', required=True, help='Path to the destination.')
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
@debug_logging
@handle_exceptions
def migrate(ctx, source, destination):
    """Perform migration of one swarm from one framework called 'source' to another framework called 'destination'."""
    swarm_cli = SwarmCLI(ctx.obj["base_url"])
    swarm_cli.migrate(source, destination)
    click.echo(f"Migration from {source} to {destination} completed.")
