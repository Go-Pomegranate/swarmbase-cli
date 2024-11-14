import os
import logging
from pydantic import BaseModel, Field
from langchain_community.tools import DeleteFileTool
from agency_swarm.tools import ToolFactory

deleteFileTool = ToolFactory.from_langchain_tool(DeleteFileTool)

class DeleteFileCommand(BaseModel):
    """Class to handle file deletion operations."""

    file_path: str = Field(..., description="The path of the file to be deleted.")

    def run(self):
        """Executes the file deletion."""
        try:
            if os.path.exists(self.file_path):
                os.remove(self.file_path)
                logger.info(f"File {self.file_path} deleted successfully.")
                return f"File {self.file_path} deleted successfully."
            else:
                logger.error(f"File {self.file_path} does not exist.")
                return f"File {self.file_path} does not exist."
        except Exception as e:
            logger.error(f"An error occurred while deleting the file: {str(e)}")
            return f"An error occurred: {str(e)}"

# Initialize logger
logger = logging.getLogger(__name__)
