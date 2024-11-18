from langchain_community.tools import ReadFileTool
from agency_swarm.tools import ToolFactory

readFileTool = ToolFactory.from_langchain_tool(ReadFileTool)
