from agency_swarm.agents import Agent
from dotenv import load_dotenv
import os
from migrator.utils.instruction_gluer.instructions_utils import InstructionGluer

# Load environment variables from .env file
load_dotenv()

class Overseer(Agent):
    def __init__(self):
        # Retrieve the model from the environment variable
        model = os.getenv('OPENAI_MODEL')

        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Construct the absolute paths
        instructions_path = os.path.join(current_dir, "instructions.md")
        tools_folder_path = os.path.join(current_dir, "tools")
        
        # Print the current directory, instructions path, and tools folder path for debugging
        print(f"Current directory: {current_dir}")
        print(f"Instructions path: {instructions_path}")
        print(f"Tools folder path: {tools_folder_path}")
        
        instruction_gluer_enabled = os.getenv('INSTRUCTION_GLUER_ENABLED')
        if instruction_gluer_enabled:
            instruction_gluer = InstructionGluer("./Overseer/instructions.md", "./Overseer/instructions_examples")
            instruction_gluer.insert_code_into_md()
        
        super().__init__(
            name="Overseer",
            description="Responsible for overseeing the whole process of making of the migration script in case of completeness of the domains such as swarms, tools, agents, frameworks etc.",
            tools_folder=tools_folder_path,
            instructions=instructions_path,
            tools=[],
            model=model,  # Use the model from the environment variable
        )