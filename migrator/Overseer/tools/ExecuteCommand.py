from agency_swarm import BaseTool
from pydantic import Field
import subprocess
import logging

logger = logging.getLogger(__name__)

class ExecuteCommand(BaseTool):
    """Run any command from the terminal. If there are too many logs, the outputs might be truncated."""

    command: str = Field(..., description="The command to be executed.")

    def run(self):
        """Executes the given command and captures its output and errors."""
        try:
            # Splitting the command into a list of arguments
            command_args = self.command.split()

            # Logging the attempt to execute the command
            logger.info(f"Executing command: {' '.join(command_args)}")

            # Executing the command
            result = subprocess.run(
                command_args, text=True, capture_output=True, check=True
            )
            # Logging the successful execution
            logger.info(f"Command executed successfully: {result.stdout}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            # Logging the error
            logger.error(f"Command execution failed: {e.stderr}")
            return f"An error occurred: {e.stderr}"
