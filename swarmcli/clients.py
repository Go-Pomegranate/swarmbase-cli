"""SwarmCLI Client."""

from abc import ABC
from typing import Any, Dict

from .utils import make_request


class BaseClient(ABC):
    def __init__(self, base_url: str, resource: str):
        self.base_url = f"{base_url}/api/{resource}"

    def create(self, data: Dict[str, Any]):
        return make_request("POST", self.base_url, data=data)

    def list(self):
        return make_request("GET", self.base_url)

    def get(self, resource_id: str):
        url = f"{self.base_url}/{resource_id}"
        return make_request("GET", url)

    def update(self, resource_id: str, data: Dict[str, Any]):
        url = f"{self.base_url}/{resource_id}"
        return make_request("PUT", url, data=data)

    def delete(self, resource_id: str):
        url = f"{self.base_url}/{resource_id}"
        return make_request("DELETE", url)


class AgentClient(BaseClient):
    def __init__(self, base_url: str):
        super().__init__(base_url, "agents")

    def assign_tool_to_agent(self, agent_id: str, tool_data: Dict[str, Any]):
        url = f"{self.base_url}/{agent_id}/tools"
        return make_request("POST", url, data=tool_data)

    def remove_tool_from_agent(self, agent_id: str, tool_data: Dict[str, Any]):
        url = f"{self.base_url}/{agent_id}/tools"
        return make_request("DELETE", url, data=tool_data)

    def get_tools(self, agent_id: str):
        url = f"{self.base_url}/{agent_id}/tools"
        return make_request("GET", url)

    def add_relationship(self, agent_id: str, data: Dict[str, Any]):
        url = f"{self.base_url}/{agent_id}/relationships"
        return make_request("POST", url, data=data)

    def get_relationships(self, agent_id: str):
        url = f"{self.base_url}/{agent_id}/relationships"
        return make_request("GET", url)

    def remove_relationship(self, agent_id: str, related_agent_id: str):
        url = f"{self.base_url}/{agent_id}/relationships/{related_agent_id}"
        return make_request("DELETE", url)


class FrameworkClient(BaseClient):
    def __init__(self, base_url):
        super().__init__(base_url, "frameworks")

    def add_swarm_to_framework(
        self,
        framework_id: str,
        swarm_data: Dict[str, Any],
    ):
        url = f"{self.base_url}/{framework_id}/swarms"
        return make_request("POST", url, data=swarm_data)

    def remove_swarm_from_framework(
        self,
        framework_id: str,
        swarm_data: Dict[str, Any],
    ):
        url = f"{self.base_url}/{framework_id}/swarms"
        return make_request("POST", url, data=swarm_data)

    def add_tool_to_framework(self, framework_id: str, tool_data):
        url = f"{self.base_url}/{framework_id}/tools"
        return make_request("POST", url, data=tool_data)


class SwarmClient(BaseClient):
    def __init__(self, base_url):
        super().__init__(base_url, "swarms")


class ToolClient(BaseClient):
    def __init__(self, base_url):
        super().__init__(base_url, "tools")
