import logging
import subprocess
import os
import requests
import json
from agency_swarm import set_openai_key
from agency_swarm import BaseTool
from pydantic import Field
from agency_swarm import Agent, Agency
from agency_swarm.tools import BaseTool


def setup_logger(name, log_file, level=logging.INFO):
    """Function to setup as many loggers as you want"""

    # Create a custom logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create handlers
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)

    # Create formatters and add it to handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)

    return logger


# Usage
logger = setup_logger("operation", "operation.log")


def get_root_tree_output():
    try:
        # Run the 'tree' command and capture its output
        result = subprocess.run(
            ["tree", "-L", "1", "-a"], capture_output=True, text=True, check=True
        )
        return result.stdout  # Returns the output of the tree command as a string
    except subprocess.CalledProcessError as e:
        return f"Failed to execute tree command: {e.stderr}"  # Handle errors


def get_project_tree_output():
    try:
        # Run the 'tree' command and capture its output
        result = subprocess.run(
            ["tree", "-L", "1", "-a", "VA"], capture_output=True, text=True, check=True
        )
        return result.stdout  # Returns the output of the tree command as a string
    except subprocess.CalledProcessError as e:
        return f"Failed to execute tree command: {e.stderr}"  # Handle errors


def get_project_important_folders(folders: list[str]) -> list[str]:
    folder_structure = []
    for folder in folders:
        try:
            # Run the 'tree' command and capture its output
            result = subprocess.run(
                ["tree", "-L", "3", "-I", "__pycache__|tests", folder],
                capture_output=True,
                text=True,
                check=True,
            )
            # Clean the output by replacing non-breaking spaces with regular spaces
            cleaned_output = result.stdout.replace("\xa0", " ")
            # Append the cleaned output of the tree command to the list, removing the last line (which is a summary of directories)
            folder_structure.append("\n".join(cleaned_output.split("\n")[:-2]))
        except subprocess.CalledProcessError as e:
            folder_structure.append(
                f"Failed to execute tree command for folder '{folder}': {e.stderr}"
            )  # Handle errors
    return folder_structure


agency_manifesto = """
Agency Manifesto
You are a part of company named swarmbase.ai. Swarmbase.ai is a company that offer the platform to aggregate, maintain and develop multi-agents swarms on scale
"""


class SendMessageToGChat(BaseTool):
    message: str = Field(..., description="Message to send to Google Chat")

    def run(self):
        headers = {"Content-Type": "application/json; charset=UTF-8"}
        payload = {"text": self.message}
        response = requests.post(
            "https://chat.googleapis.com/v1/spaces/AAAAi8jcYlY/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=KbSLqqQq7M-At25-LIg9D75ZjuVBsm6UN-hft1WDL8M",
            headers=headers,
            data=json.dumps(payload),
        )

        if response.status_code == 200:
            return "Message sent to GChat successfully."
        else:
            return f"Failed to send message to GChat. Status code: {response.status_code}, Response: {response.text}"


class File(BaseTool):
    """
    File to be written to the disk with an appropriate name and file path, containing code that can be saved and executed locally at a later time.
    """

    file_name: str = Field(
        ...,
        description="The name of the file including the extension and the file path from your current directory if needed.",
    )
    body: str = Field(..., description="Correct contents of a file")

    def run(self):
        # Extract the directory path from the file name
        directory = os.path.dirname(self.file_name)

        # If the directory is not empty, check if it exists and create it if not
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        # Write the file
        with open(self.file_name, "w") as f:
            f.write(self.body)

        return "File written to " + self.file_name


class Program(BaseTool):
    """
    Set of files that represent a complete and correct program. This environment has access to all standard Python packages and the internet.
    """

    chain_of_thought: str = Field(
        ...,
        description="Think step by step to determine the correct actions that are needed to implement the program.",
    )
    files: list[File] = Field(..., description="List of files")

    def run(self):
        outputs = []
        for file in self.files:
            outputs.append(file.run())

        return str(outputs)


def replace_bracketed_word(text, word_to_replace, replacement_word):
    """
    Replaces all occurrences of a word in brackets with a specified replacement word.

    :param text: The input text containing words in brackets.
    :param word_to_replace: The word inside brackets to be replaced.
    :param replacement_word: The word to replace the bracketed word with.
    :return: The modified text with replacements.
    """
    # Construct the pattern to search for
    pattern = f"[{word_to_replace}]"

    # Replace occurrences of the pattern with the replacement word
    modified_text = text.replace(pattern, replacement_word)

    return modified_text


from migrator.DomainWorker.Agents.AgentsWorker import AgentsDomainWorker
from migrator.DomainWorker.Swarm.SwarmsWorker import SwarmsDomainWorker
from migrator.DomainWorker.Framework.FrameworksWorker import FrameworksDomainWorker
from migrator.DomainWorker.Tools.ToolsWorker import ToolsDomainWorker
from migrator.Overseer import Overseer
from migrator.Supervisor import Supervisor


class Migrator:
    """
    Migrator class responsible for migrating data or files.
    """

    def __init__(self):
        """
        Initializes the migrator.
        """
        self.agency = self._create_agency()

    def _create_agency(self):
        """
        Creates and returns a predefined Agency instance.
        """
        supervisor = Supervisor()
        overseer = Overseer()
        swarmsDomainWorker = SwarmsDomainWorker()
        frameworksDomainWorker = FrameworksDomainWorker()
        toolsDomainWorker = ToolsDomainWorker()
        agentsDomainWorker = AgentsDomainWorker()

        agency_manifesto = """
        Agency Manifesto
        You are a part of company named swarmbase.ai. Swarmbase.ai is a company that offer the platform to aggregate, maintain and develop multi-agents swarms on scale
        """

        return Agency(
            [
                supervisor,
                [supervisor, overseer],
                [overseer, supervisor],
                [overseer, swarmsDomainWorker],
                [overseer, frameworksDomainWorker],
                [overseer, agentsDomainWorker],
                [overseer, toolsDomainWorker],
            ],
            shared_instructions=agency_manifesto,
        )

    def migrate(self, source, destination):
        """
        Method to perform the migration and trigger the agency.

        :param source: Path to the source data.
        :param destination: Path to the destination.
        """
        self.source = source
        self.destination = destination

        try:
            # Example migration logic
            print(f"Migration from {self.source} to {self.destination} started.")

            # Trigger the agency
            self.agency.demo_gradio(height=900)

            print("Migration completed successfully.")
        except Exception as e:
            print(f"Error during migration: {e}")


if __name__ == "__main__":
    set_openai_key("")
    source_path = "/Users/pantere/Repositories/private/projects/swarmbase/VA/migrator/tests/simulations/sim2"
    destination_path = "/Users/pantere/Repositories/private/projects/swarmbase/VA/migrator/tests/simulations/sim2"

    migrator = Migrator()
    migrator.migrate(source_path, destination_path)
