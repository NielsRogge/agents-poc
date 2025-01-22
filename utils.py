import os
from typing import List
from components import AgentConfig, Tool


def load_agent_config(filename):
    """Load agent configuration from a text file"""
    config = {}
    with open(os.path.join('agents', filename)) as f:
        for line in f:
            key, value = line.strip().split(': ', 1)
            config[key] = value
    return config


def create_transfer_tool(downstream_agents: List[AgentConfig]) -> Tool:
    """Creates a tool for transferring to other agents"""
    available_agents_list = "\n".join([
        f"- {agent.name}: {agent.public_description}"
        for agent in downstream_agents
    ])
    
    return {
        "type": "function",
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
                    "description": "The reasoning why this transfer is needed."
                },
                "conversation_context": {
                    "type": "string", 
                    "description": "Relevant context from the conversation."
                },
                "destination_agent": {
                    "type": "string",
                    "description": "The destination agent to handle the request.",
                    "enum": [agent.name for agent in downstream_agents]
                }
            },
            "required": ["rationale_for_transfer", "conversation_context", "destination_agent"]
        }
    }