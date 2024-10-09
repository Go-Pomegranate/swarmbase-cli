from typing import Any, Dict, Optional

from swarmcli.utils import RelationshipType

from .builders import AgentBuilder, FrameworkBuilder, SwarmBuilder, ToolBuilder
from .clients import AgentClient, FrameworkClient, SwarmClient, ToolClient


class SwarmCLI:
    def __init__(self, base_url):
        self.agent_client = AgentClient(base_url)
        self.framework_client = FrameworkClient(base_url)
        self.swarm_client = SwarmClient(base_url)
        self.tool_client = ToolClient(base_url)

    # Metody bezpośredniego tworzenia
    def create_agent(
        self,
        name: str,
        description: Optional[str] = None,
        instructions: Optional[str] = None,
        extra_attributes: Optional[Dict[str, Any]] = None,
    ):
        data = {
            "name": name,
            "description": description,
            "instructions": instructions,
            "extra_attributes": extra_attributes,
        }
        return self.agent_client.create(data)

    def list_agents(self):
        return self.agent_client.list()

    def get_agent(self, agent_id: str):
        return self.agent_client.get(agent_id)

    def update_agent(
        self,
        agent_id: str,
        name: str,
        description: Optional[str] = None,
        instructions: Optional[str] = None,
        extra_attributes: Optional[Dict[str, Any]] = None,
    ):
        data = {
            "name": name,
            "description": description,
            "instructions": instructions,
            "extra_attributes": extra_attributes,
        }
        return self.agent_client.update(agent_id, data)

    def delete_agent(self, agent_id: str):
        return self.agent_client.delete(agent_id)

    def add_agent_relationship(
        self,
        agent_id: str,
        related_agent_id: str,
        relationship_type: RelationshipType,
    ):
        data = {
            "related_agent_id": related_agent_id,
            "relationship_type": relationship_type,
        }
        return self.agent_client.add_relationship(agent_id, data)

    def get_agent_relationships(self, agent_id: str):
        return self.agent_client.get_relationships(agent_id)

    def remove_agent_relationship(
        self,
        agent_id: str,
        related_agent_id: str,
    ):
        return self.agent_client.remove_relationship(
            agent_id,
            related_agent_id,
        )

    def assign_tool_to_agent(self, agent_id: str, tool_data: Dict[str, Any]):
        return self.agent_client.assign_tool_to_agent(agent_id, tool_data)

    def remove_tool_from_agent(self, agent_id: str, tool_id: str):
        tool_data = {"tool_id": tool_id}
        return self.agent_client.remove_tool_from_agent(agent_id, tool_data)

    def get_agent_tools(self, agent_id: str):
        return self.agent_client.get_tools(agent_id)

    def create_framework(self, name: str, description: Optional[str] = None):
        data = {"name": name, "description": description}
        return self.framework_client.create(data)

    def list_frameworks(self):
        return self.framework_client.list()

    def get_framework(self, framework_id: str):
        return self.framework_client.get(framework_id)

    def update_framework(
        self, framework_id: str, name: str, description: Optional[str] = None
    ):
        data = {"name": name, "description": description}
        return self.framework_client.update(framework_id, data)

    def delete_framework(self, framework_id: str):
        return self.framework_client.delete(framework_id)

    def assign_swarm_to_framework(self, framework_id: str, swarm_id: str):
        return self.framework_client.add_swarm_to_framework(
            framework_id,
            swarm_id,
        )

    def remove_swarm_from_framework(self, framework_id: str, swarm_id: str):
        return self.framework_client.remove_swarm_from_framework(
            framework_id,
            swarm_id,
        )

    def create_swarm(
        self,
        name: str,
        parent_id: Optional[str] = None,
        extra_attributes: Optional[Dict[str, Any]] = None,
    ):
        data = {
            "name": name,
            "parent_id": parent_id,
            "extra_attributes": extra_attributes,
        }
        return self.swarm_client.create(data)

    def list_swarms(self):
        return self.swarm_client.list()

    def get_swarm(self, swarm_id: str):
        return self.swarm_client.get(swarm_id)

    def update_swarm(self, swarm_id: str, name: str, description: Optional[str] = None):
        data = {"name": name, "description": description}
        return self.swarm_client.update(swarm_id, data)

    def delete_swarm(self, swarm_id: str):
        return self.swarm_client.delete(swarm_id)

    def create_tool(
        self,
        name: str,
        description: Optional[str] = None,
        version: Optional[str] = None,
        code: Optional[str] = None,
        extra_attributes: Optional[Dict[str, Any]] = None,
    ):
        data = {
            "name": name,
            "description": description,
            "version": version,
            "code": code,
            "extra_attributes": extra_attributes,
        }
        return self.tool_client.create(data)

    def list_tools(self):
        return self.tool_client.list()

    def get_tool(self, tool_id: str):
        return self.tool_client.get(tool_id)

    def update_tool(
        self,
        tool_id: str,
        name: str,
        description: Optional[str] = None,
        version: Optional[str] = None,
        code: Optional[str] = None,
        extra_attributes: Optional[Dict[str, Any]] = None,
    ):
        data = {
            "name": name,
            "description": description,
            "version": version,
            "code": code,
            "extra_attributes": extra_attributes,
        }
        return self.tool_client.update(tool_id, data)

    def delete_tool(self, tool_id: str):
        return self.tool_client.delete(tool_id)

    # Metody buildera
    def agent_builder(self):
        return AgentBuilder(self.agent_client)

    def framework_builder(self):
        return FrameworkBuilder(self.framework_client)

    def swarm_builder(self):
        return SwarmBuilder(self.swarm_client)

    def tool_builder(self):
        return ToolBuilder(self.tool_client)
