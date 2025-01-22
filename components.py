
from dataclasses import dataclass
from typing import TypedDict, List, Optional, Literal


class Tool(TypedDict):
    type: Literal["function"]
    name: str
    description: str
    parameters: dict


@dataclass
class AgentConfig:
    name: str
    public_description: str
    instructions: str
    tools: List[Tool]
    downstream_agents: Optional[List['AgentConfig']] = None