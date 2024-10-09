"""Swarm CLI builders."""

from dataclasses import asdict, field
from datetime import datetime
from typing import Any, ClassVar, Dict, Generic, List, NamedTuple, Optional, TypeVar

from pydantic import ConfigDict, field_validator
from pydantic.dataclasses import dataclass

from .utils import RelationshipType
from .clients import (
    AgentClient,
    BaseClient,
    FrameworkClient,
    SwarmClient,
    ToolClient,
)
import re
import keyword


@dataclass
class Product:
    id: Optional[str] = None
    _name: str = field(init=False)
    extra_attributes: Dict[str, Any] = field(default_factory=dict)

    @field_validator("_name")
    def validate_variable_name(cls, v: str) -> str:
        """Validate whether _name can be used as a valid Python identifier."""
        if not re.match(r"^[a-zA-Z_]\w*$", v):
            raise ValueError("Provided name is not a valid Python identifier.")
        if keyword.iskeyword(v):
            raise ValueError("Provided name is a reserved keyword in Python.")

        return v

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    def __post_init__(self):
        self.name = self.__class__.__name__


T = TypeVar("T", bound="Product")


@dataclass(
    config=ConfigDict(arbitrary_types_allowed=True, revalidate_instances="always"),
)
class BaseBuilder(Generic[T]):
    client: BaseClient
    _product_type: Any = field(init=False)
    _product: T = field(init=False)

    def __post_init__(self):
        self._product = self._product_type()

    def set_id(self, id: str):
        self._product.id = id
        return self

    def set_name(self, name: str):
        self._product.name = name
        return self

    def set_extra_attributes(self, extra_attributes):
        self._product.extra_attributes = extra_attributes
        return self

    def build(self):
        return self.client.create(asdict(self._product))

    @property
    def product(self) -> T:
        return self._product


@dataclass
class Tool(Product):
    tool_count: ClassVar[int] = 0
    description: Optional[str] = None
    version: Optional[str] = None
    code: Optional[str] = None

    def __post_init__(self):
        Tool.tool_count += 1

    def as_string(self):
        "Tool representation as BaseTool from agency swarm."
        tool_description = f'"""{self.description}"""' if self.description else ""
        tool_name = (
            self.name if (self.name or self.name == "") else f"Tool{Tool.tool_count}"
        )
        tool_class = f"""class {tool_name}(BaseTool):
    {tool_description}
    {self.code}
        """
        return tool_class


@dataclass
class ToolBuilder(BaseBuilder[Tool]):
    client: ToolClient

    def __post_init__(self):
        self._product_type = Tool
        super().__post_init__()

    def set_description(self, description):
        self._product.description = description

    def set_version(self, version):
        self._product.version = version

    def set_code(self, code):
        self._product.code = code

    def from_id(self, id: str):
        data = self.client.get(id)
        if data:
            self.set_id(data.get("id"))
            self.set_description(data.get("description"))

            self.set_extra_attributes(data.get("extra_attributes"))
            newest_code_data = sorted(
                data["code_versions"],
                key=lambda item: datetime.strptime(
                    item["created_at"], "%Y-%m-%dT%H:%M:%S.%f"
                ),
            )[0]
            self.set_version(newest_code_data.get("version"))
            self.set_code(newest_code_data.get("code"))
        return self


class AgentRelationship(NamedTuple):
    relationship_type: RelationshipType
    source_agent_id: str
    target_agent_id: str


@dataclass
class Agent(Product):
    agent_count: ClassVar[int] = 0
    description: Optional[str] = None
    instuctions: Optional[str] = None
    relationships: List[AgentRelationship] = field(default_factory=list)
    tools: List[Tool] = field(default_factory=list)

    def __post_init__(self):
        Agent.agent_count += 1

    def as_string(self):
        """Agent representation as agent from agency swarm."""
        agent_description = f'"""{self.description}"""' if self.description else ""
        agent_name = self.name if self.name else f"agent{Agent.agent_count}"
        agent_instructions = self.instuctions if self.instuctions else f""
        agent_class = f"""{agent_name} = Agent(
        name={agent_name},
        description="{agent_description}",
        instuctions=\"\"\"{agent_instructions}\"\"\",
        tools={[tool.name for tool in self.tools]}
        model="{[self.extra_attributes.get("model", "gpt-4o")]}"
        """
        return agent_class


@dataclass
class AgentBuilder(BaseBuilder[Agent]):
    client: AgentClient

    def set_description(self, description: str):
        self._product.description = description
        return self

    def set_instructions(self, instuctions: str):
        self._product.instuctions = instuctions
        return self

    def add_relationship(self, relationship: AgentRelationship):
        self._product.relationships.append(relationship)
        return self

    def add_tool(self, tool: Tool):
        self._product.tools.append(tool)
        return self

    def from_id(self, id: str):
        data = self.client.get(id)
        tool_builder = ToolBuilder(ToolClient(self.client.base_url))

        if data:
            self.set_id(data.get("id"))
            self.set_description(data.get("description"))
            self.set_instructions(data.get("instructions"))
            self.set_extra_attributes(data.get("extra_attributes"))

            for _ in data.get("relationships"):
                relationship = AgentRelationship(
                    RelationshipType(_["relationship_type"]),
                    _.get["source_agent_id"],
                    _.get["target_agent_id"],
                )
                self.add_relationship(relationship)

            for tool_id in data.get("tools"):
                self.add_tool(tool_builder.from_id(tool_id).product)

        return self


@dataclass
class Framework(Product):
    pass


@dataclass
class FrameworkBuilder(BaseBuilder[Framework]):
    client: FrameworkClient
    _product: Framework


@dataclass
class Swarm(Product):
    parent_id: Optional[str] = None
    agents: List[Agent] = field(default_factory=list)


@dataclass
class SwarmBuilder(BaseBuilder[Swarm]):
    client: SwarmClient

    def add_agent(self, agent: Agent):
        self._product.agents.append(agent)
        return self

    def from_id(self, id: str):
        data = self.client.get(id)
        if data:
            self.set_id(data.get("id"))
            self.set_name(data.get("name"))

            agent_builder = AgentBuilder(AgentClient(self.client.base_url))

            for agent_data in data.get("agents"):
                agent: Agent = agent_builder.from_id(agent_data.get("id")).product
                self.add_agent(agent)

            self.set_extra_attributes(data.get("extra_attributes"))

        return self
