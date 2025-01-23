import os
from typing import List
from components import Agent, Tool
import json


def get_agent(agent_name: str) -> Agent:
    """Load agent configuration from a JSON file and return an Agent object"""
    filepath = os.path.join("agents", f"{agent_name}.json")
    with open(filepath) as f:
        config = json.load(f)
    return Agent(
        name=config["name"],
        public_description=config["description"],
        instructions=config["instructions"],
        tools=[],
    )


def create_transfer_tool(downstream_agents: List[Agent]) -> Tool:
    """Creates a tool for transferring to other agents"""
    available_agents_list = "\n".join(
        [
            f"- {agent.name}: {agent.public_description}"
            for agent in downstream_agents
        ]
    )

    return {
        "type": "function",
        "function": {
            "name": "transferAgents",
            "description": f"""Triggers a transfer of the user to a more specialized agent.
                        Available Agents:
                        {available_agents_list}
                        """,
            "parameters": {
                "type": "object",
                "properties": {
                    "rationale_for_transfer": {
                        "type": "string",
                        "description": "The reasoning why this transfer is needed.",
                    },
                    "conversation_context": {
                        "type": "string",
                        "description": "Relevant context from the conversation.",
                    },
                    "destination_agent": {
                        "type": "string",
                        "description": "The destination agent to handle the request.",
                        "enum": [agent.name for agent in downstream_agents],
                    },
                },
                "required": [
                    "rationale_for_transfer",
                    "conversation_context",
                    "destination_agent",
                ],
            },
        },
    }
