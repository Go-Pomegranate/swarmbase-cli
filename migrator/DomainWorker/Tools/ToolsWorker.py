from agency_swarm.agents import Agent
from dotenv import load_dotenv
import os
from migrator.utils.instruction_gluer.instructions_utils import InstructionGluer

# Load environment variables from .env file
load_dotenv()

class ToolsDomainWorker(Agent):
    def __init__(self):
        # Retrieve the model from the environment variable
        model = os.getenv('OPENAI_MODEL')
        instruction_gluer_enabled = os.getenv('INSTRUCTION_GLUER_ENABLED')
        if instruction_gluer_enabled:
            instruction_gluer = InstructionGluer("./DomainWorker/Tools/instructions.md", "./DomainWorker/Tools/instructions_examples")
            instruction_gluer.insert_code_into_md()
        
        super().__init__(
            name="ToolsDomainWorker",
            description="Responsible for overseeing the whole process of making of the migration script in case of completeness of the domains such as swarms, tools, agents, frameworks etc.",
            instructions="./instructions.md",
            tools_folder="./tools",
            tools=[],
            model=model,
            files_folder = "./files"

        )