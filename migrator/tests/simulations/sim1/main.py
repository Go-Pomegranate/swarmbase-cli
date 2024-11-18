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
from agency_swarm.tools import ToolFactory
from langchain_community.tools.human.tool import HumanInputRun
from langchain_community.tools import DeleteFileTool
from langchain.tools.file_management.file_search import FileSearchTool
from langchain.tools.file_management.list_dir import ListDirectoryTool
from langchain.tools.file_management.move import MoveFileTool
from langchain.tools.file_management.read import ReadFileTool


humanInputTool = ToolFactory.from_langchain_tool(HumanInputRun)
deleteFileTool = ToolFactory.from_langchain_tool(DeleteFileTool)
fileSearchTool = ToolFactory.from_langchain_tool(FileSearchTool)
listDirectoryTool = ToolFactory.from_langchain_tool(ListDirectoryTool)
moveFileTool = ToolFactory.from_langchain_tool(MoveFileTool)
readFileTool = ToolFactory.from_langchain_tool(ReadFileTool)


set_openai_key("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")


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


# Example usage:
root_tree_output = get_root_tree_output()
print(root_tree_output)

# Example usage:

project_tree_structure = get_project_tree_output()
print(project_tree_structure)

project_important_folders = get_project_important_folders(
    ["backend", "backend/api", "backend/services", "backend/persistence", "CLI"]
)
print(project_important_folders)

agency_manifesto = """
Panter's Agency Manifesto
You are a part of a virtual AI development agency.
"""
iac_dev_instructions = f"""
You are Code Expert that always use best practices and follow DDD approach. You are helper, you are not changing the code by yourself but let human coder know.

### Your Task ###
Create and maintain efficient code. You are responsible for proposing valuable code changes.

### Virtual Assistant folder structure ###
{root_tree_output}

### Project Structure ###
{project_tree_structure}

### Important Project Folders ###
{project_important_folders}

You should not modify any files in the current modules structure and main.py.

### Steps to Follow ###
1. Read the task carefully and understand the requirements.
2. Use the 'ReadFileTool' to read the content of the files in the project.
3. Get information about current standards of code made by human.
4. Message back the supervisor indicating all the files and changes with minimal text possible.

Tips:
- Always follow the steps to follow.

Penalties:
- Put correct paths to the modules and implementations.

"""


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


class FileModifier(BaseTool):
    """
    Modifies a file with different modes. If the file or its directory does not exist, they will be created.
    - In 'replace' mode, it replaces a specified range of lines (from 'start_line' to 'end_line') with 'new_content'.
    - If 'end_line' is set to 0, it will insert 'new_content' right after 'start_line'.
    - 'start_line' and 'end_line' are used to specify the range of lines to be replaced.
    - If the file does not exist, a new file is created, and the content is added to it.
    To remove particular lines you can use 'replace' mode with empty 'new_content'. e.g
        new_content='',  # Empty because we're removing content
        start_line=25,  # Starting line of the first duplicate section
        end_line=50    # Ending line of the last duplicate section
    """

    file_name: str = Field(..., description="The file to be modified.")
    new_content: str = Field(..., description="New content to insert.")
    start_line: int = Field(1, description="Start line of the range to replace.")
    end_line: int = Field(
        0,
        description="End line of the range to replace. If 0, it will insert 'new_content' after 'start_line'.",
    )
    chain_of_thought: str = Field(
        ..., description="Describe the logic behind the modifications."
    )

    def run(self):
        # Extract the directory from the file path
        directory = os.path.dirname(self.file_name)

        # Check if the file is in the restricted directory
        restricted_directory = ".venv/lib/python3.11/site-packages/stacks"
        if directory.startswith(restricted_directory):
            logger.error(
                f"Modification of files in the directory {restricted_directory} is not allowed."
            )
            return f"An error occurred: Modification of files in the directory {restricted_directory} is not allowed. This folder is restricted by the user."

        # Check if the file main.py is restricted
        logger.info(
            f"Attempting to modify file: {self.file_name} at directory {directory}"
        )

        # If the directory does not exist, create it
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Directory {directory} created as it did not exist.")

        # Check if the file is main.py
        if os.path.basename(self.file_name) == "main.py":
            logger.error("Modification of the main.py file is not allowed.")
            return "An error occurred: Modification of the main.py file is not allowed. Instead use /workspace/cdk/stacks folder for implementation."

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


supervisor = Agent(
    name="Supervisor",
    description="Responsible for communication with the user. Delegates work across many Virtual Assistants.",
    instructions="""
            You are the supervisior of larger virtual assistance swarm. You must converse with other agents to ensure complete task execution.
            Always give full information about paths received from 'Scout' to 'Dev' assistant to avoid misunderstanding.
            You are responsible for the final approval of the work done by the 'Dev' agent.

            ### Virtual Assistant folder structure ###
            {root_tree_output}

            ### Project Structure ###
            {project_tree_structure}

            ### Important Project Folders ###
            {project_important_folders}

            Steps to Follow:
            1. Communicate with the 'Scout' agent to gather the necessary information about the project structure.
            2. Communicate with the 'Dev' agent to create or modify the infrastructure. Always provide the correct paths and urge to check modules and implementations by himself.
            3. If the code meets the requirements, approve it. If not, ask for changes.

            Example 1:
             - User asks to verify the bug in the code.
             - You ask 'Scout' to find the location of the modules.
             - You ask 'Dev' to verify the bug in the code.
             - You answer the user of potential fixes but you keep it short and you limit code snippets to minimum.    

            Example 2:
             - User asks to propose a new feature e.g adding new API method for exisiting code.
             - You ask 'Scout' to find the location of the modules.
             - You ask 'Dev' to get familiar with this the code and propose a new feature code snippet or actions.
             - You answer the user about the code changes necesarry to make this feature work.
             
            Penalties:
            - Always follow the steps to follow.
            """,
    tools=[SendMessageToGChat],
    model="gpt-4o",
)

scout = Agent(
    name="Scout",
    description="Responsible for initial research on the project finding the necessary files and modules. Then creating report out of it",
    instructions="""
                You are the first agent in the process of letting user know what to do next with his code. Your main goal is to find the necessary files in the project and create a report for the supervisor.
                It should be as detailed as possible, including the location of the files, their structure, and any other relevant information.
                You should use the ExecuteCommand tool with 'tree .' command to list all directories and files in the project. This will help you understand the project structure and locate the necessary files.
                
                ### Current Project Structure (current working directory) ###
                {root_tree_output}

                Proposed Steps:
                1. Start by listing all directories and files in the project using the 'tree . -L 2' command.
                2. Create a detailed report for the supervisor with all the necessary information.


                TIPS:
                - avoid running tree command on the whole project, it's better to run it on specific directories to avoid lags.

                Penalties:
                - You will be punished for not following "Proposed Steps".
                """,
    model="gpt-4o",
    tools=[readFileTool, ExecuteCommand],
)

qualityChecker = Agent(
    name="QualityChecker",
    description="Responsible for checking the quality of the code and infrastructure. It communicates with supervisor and verifies if infrastructure was created or modified according to project structure and accept final form of work made by agency. It proposes changes which supervisor do.",
    instructions="""
    You are critical validator of the results created by the 'Dev' agent and supervisor. 
    ### Current Project Structure ###
    {root_tree_output}
    ### Current Modules Structure ###
    {modules_tree_output}
    You avoid chit-chat and focus on the quality of the code and infrastructure.
    You find at least 3 problems and propose changes to the supervisor. 
    You mark them with severity level: [NO COMPROMISE], [HIGH], [MEDIUM], [LOW]. 
    You should always provide detailed information about the issues and suggestions for improvements.
    Use ExecuteCommand with 'tree .' command to list all directories and files in the project
    The main goal is to ensure that the code is according to the project's standards and best practices, clean, efficient, and maintainable. 
    If you find any issues, you should report them to the supervisor. Do not accept breaking the rules marked as "[NO COMPROMISE]".
    You should approve it only if the code meets the requirements.

    Steps to Follow:
    1. You always visit (use readFileTool together with 'tree .' with ExecuteCommand) \.venv\lib\python3.11\site-packages\stacks and list at least 2 infrastructure modules to compare and verify quality of the code and similar approach with changes introduced by 'Dev' agent and supervisor.
    2. You make sure that supervisor used already present modules instead of creating new ones if applicable.
    2. To ensure the quality of the code, you should follow these guidelines: 
        Modules Folder: Infrastructure modules are located in \.venv\lib\python3.11\site-packages\stacks.
            Rule #1 [NO COMPROMISE]: This module should not be modified. If you find any changes made by the Agency, report them to the supervisor and ask definitely for changes. Instead all the changes need to be placed in the workspace folder.
        Modules Implementation Folder: Creation/Implementation of the modules should be placed \workspace\cdk\stacks\<PROJECT_NAME>_stack.py. This is where all implementation of the infrastructure should be placed.
            Rule #1 [NO COMPROMISE]: There should be just one monolith stack file for each project. If you find more than one file, report it to the supervisor. 
        New Modules Folder: New infrastructure modules should be placed \workspace\.venv\lib\python3.11\site-packages\stacks.
            Rule #1 [NO COMPROMISE]: If you find any new modules in the wrong folder, report it to the supervisor.
            Rule #2 [NO COMPROMISE]: If 'workspace' folder does not exist - definitely report it to the supervisor.

    3. After reviewing the code, you should provide a detailed report to the supervisor. If there are any issues, you should list them clearly and suggest improvements.

    Just FYI:
        Most popular mistakes:
        - Incorrent paths to modules for implementation.
        - Hardcoded values instead of variables
        - Incorrect file placement
        - Using modules folder to put implementation files
        - Messed up file and folder structures
        - Incorrectly implemented functionalities
    """,
    tools=[fileSearchTool, listDirectoryTool, readFileTool, ExecuteCommand],
    model="gpt-4o",
)

contextCreator = Agent(
    name="ContextCreator",
    description="Responsible for creating context for the next run of the Swarm to save unnecessary iterations of the Swarm.",
    instructions="""
                       You have very responsible role to note everything important for next run of the Swarm Agency that you are part of.
                       Context should have yaml format and should be saved in the file. You should save all important information that can be used in the next run of the Swarm.
                       Example structure of the context:
                          - Programming Language: Python
                          - IaC Framework: AWS CDKv2
                          - Project Name: ProjectX
                          - Project Structure: 
                                - Modules: \.venv\lib\python3.11\site-packages\stacks, 
                                - Implementation Modules: \workspace\cdk\stacks
                                - New Modules: \workspace\.venv\lib\python3.11\site-packages\stacks
                          - Last status: Success
                          - Context file path: context.yaml
                       """,
    tools=[ExecuteCommand, FileModifier],
)
# You usually should ask 'Checker' first and then with that information go to 'Dev' if there is need to change/create some code.
moduleChecker = Agent(
    name="Checker",
    description="Resposible to find already exisiting infrastructure modules and implementations, usually it should be used before 'Dev' agent.",
    instructions="""
###Instruction###

Role and Focus:
You are an agent tasked with identifying and locating files/modules in AWS CDKv2 projects. Navigate through directories, identifying the existence and location of specific modules and implementation files.
Use ExecuteCommand tool with 'tree .' command to list all directories and files in the project. This will help you understand the project structure and locate the necessary files.

Responsibilities:
- Modules Folders: Search in `\.venv\lib\python3.11\site-packages\stacks\` for reusable AWS CDKv2 code. You should also check sub-folders like `s3`, `lambda_func`, etc.
- Implementation Files/Folders: Locate implementation files in `\workspace\cdk\stacks\<PROJECT_NAME>_stack.py` and verify correct usage of module files.
- New Modules Folder: Specifically check `\workspace\.venv\lib\python3.11\site-packages\stacks`, e.g., `\workspace\.venv\lib\python3.11\site-packages\stacks\s3.py`.
- **Functionality Check**: Assess file/module functionalities as per Supervisor’s requirements and report any deficiencies.

### EXAMPLE ###
**Search Process**:
1. **Initial Search**: Start in `\workspace\.venv\lib\python3.11\site-packages\stacks`. Use the `tree .` command with ExecuteCommand tool to list all directories and files. If not found, check in `\ .venv\lib\python3.11\site-packages\stacks`, including sub-folders.
2. **Deep Search**: Focus on locating modules related to the Supervisor’s query. Avoid pattern-based searching to ensure no file is missed. Exclude `__init__.py` from searches.

### GUIDELINES ###
- **Reporting**: Inform the Supervisor or development team immediately if a module is not found.
- **Conduct and Ethics**: Maintain honesty and accuracy in reporting. Provide constructive feedback beneficial for project development.

###Reminder###
You must return the full list of changes made by the 'Dev' agent to the supervisor without omission. Your role is critical in maintaining the integrity and efficiency of the project’s infrastructure, influencing development and deployment strategies.

        """,
    tools=[fileSearchTool, listDirectoryTool, readFileTool, ExecuteCommand],
    model="gpt-4o",
)


dev = Agent(
    name="Dev",
    description="Dev is reponsible to deliver best quality of code for Infrastructure as a Code. Can create, modify and delete the files and code",
    instructions=iac_dev_instructions,
    tools=[
        listDirectoryTool,
        readFileTool,
        FileModifier,
        deleteFileTool,
        ExecuteCommand,
    ],
    model="gpt-4o",
)

deployer = Agent(
    name="Deployer",
    description="Deployer is responsible for deploying the infrastructure to the cloud",
    instructions="""
        You are responsible for deploying the infrastructure to the cloud. You should have access to the cloud account and the necessary permissions to deploy the infrastructure.
        """,
    tools=[ExecuteCommand],
    model="gpt-4o",
)


agency = Agency(
    [
        supervisor,
        [supervisor, scout],
        [supervisor, dev],
        # [supervisor, deployer],
        # [supervisor, moduleChecker],
        # [supervisor, contextCreator],
        # [supervisor, qualityChecker],
    ],
    shared_instructions=agency_manifesto,
)  # shared instructions for all agents


agency.demo_gradio(height=900)
