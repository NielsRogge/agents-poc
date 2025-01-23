from dataclasses import dataclass, field
from typing import TypedDict, Literal, Callable


class Tool(TypedDict):
    type: Literal["function"]
    name: str
    description: str
    parameters: dict


@dataclass
class Agent:
    name: str
    public_description: str
    instructions: str
    tools: list[Tool] = field(default_factory=list)
    tool_logic: dict[str, Callable] = field(default_factory=dict)
    downstream_agents: list['Agent'] = field(default_factory=list)