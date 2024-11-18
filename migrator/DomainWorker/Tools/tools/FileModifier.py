import os
import logging
from pydantic import Field
from agency_swarm.tools import BaseTool

class FileModifier(BaseTool):
    """Class to handle file modification operations."""

    file_name: str = Field(..., description="The name of the file to be modified.")
    start_line: int = Field(..., description="The starting line number for modification.")
    end_line: int = Field(0, description="The ending line number for modification.")
    new_content: str = Field(..., description="The new content to insert into the file.")
    restricted_directories: list = Field(
        default_factory=lambda: ["/Users/pantere/Repositories/private/projects/swarmbase/VA/migrator"],
        description="List of restricted directories where modifications are not allowed."
    )

    def run(self):
        """Executes the file modification."""
        # Extract the directory from the file path
        directory = os.path.abspath(os.path.dirname(self.file_name))

        # Check if the file is in any restricted directory (but allow subdirectories)
        for restricted_directory in self.restricted_directories:
            restricted_directory = os.path.abspath(restricted_directory)
            if os.path.commonpath([directory, restricted_directory]) == restricted_directory and directory == restricted_directory:
                logger.error(
                    f"Modification of files in the directory {restricted_directory} is not allowed."
                )
                return f"An error occurred: Modification of files in the directory {restricted_directory} is not allowed. This folder is restricted by the user."

        # Check if the file exists
        file_exists = os.path.exists(self.file_name)

        # Initialize content variable
        content = []

        # If file exists, read the existing file
        if file_exists:
            with open(self.file_name, "r") as file:
                content = file.readlines()
            logger.info(f"Read content from existing file: {self.file_name}")
        else:
            # Create a new file if it does not exist
            with open(self.file_name, "w") as file:
                file.write("")
            logger.info(f"Created new file: {self.file_name}")

        # Validate line numbers
        if not (1 <= self.start_line <= len(content) + 1) or (
            self.end_line != 0 and not (1 <= self.end_line <= len(content))
        ):
            logger.error("Invalid line numbers provided.")
            return "Invalid line numbers."

        # Remove specified range and insert new content
        if self.end_line == 0:
            # If end_line is 0, insert new content after start_line
            modified_content = (
                content[: self.start_line]
                + [self.new_content]
                + content[self.start_line :]
            )
            logger.info(f"Inserting new content after line {self.start_line}")
        else:
            # Replace specified range with new content
            modified_content = (
                content[: self.start_line - 1]
                + [self.new_content]
                + content[self.end_line :]
            )
            logger.info(
                f"Replacing content from line {self.start_line} to {self.end_line}"
            )

        # Write the modified content back
        with open(self.file_name, "w") as file:
            file.writelines(modified_content)
            action = "created and written to" if not file_exists else "modified"
            logger.info(f"File {self.file_name} {action} successfully.")

        return f"File {self.file_name} {action} successfully."

# Initialize logger
logger = logging.getLogger(__name__)
