import json
import os
from openai import OpenAI

from components import AgentConfig 
from utils import load_agent_config, create_transfer_tool

# Set your OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load agent configurations
def get_agent_config(agent_name: str) -> AgentConfig:
    config = load_agent_config(f'{agent_name}.json')
    return AgentConfig(
        name=config['name'],
        public_description=config['description'],
        instructions=config['instructions'],
        tools=[],
    )


def chat_with_agent(agent_name: str, message: str, history: list[dict]) -> tuple[str, AgentConfig]:
    """Chat with an agent using the OpenAI API"""

    agent = get_agent_config(agent_name)
    
    messages = [{"role": "system", "content": agent.instructions}]
    messages.extend(history)
    messages.append({"role": "user", "content": message})
    
    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=agent.tools if agent.tools else None,
        tool_choice="auto" if agent.tools else None,
    )
    
    assistant_message = response.choices[0].message
    
    # Handle function calls
    if assistant_message.tool_calls:
        tool_call = assistant_message.tool_calls[0]
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        if function_name == "transferAgents":
            # Find the destination agent
            destination_agent = next(
                (agent for agent in agent.downstream_agents 
                 if agent.name == function_args["destination_agent"]),
                None
            )
            if destination_agent:
                print(f"Transferring to {destination_agent.name}...")
                return chat_with_agent(
                    destination_agent.name,
                    function_args["conversation_context"]
                )
    
    return assistant_message.content, agent.name


# Example usage
async def main():
    # Start conversation with greeter agent
    current_agent = "greeter"
    response, current_agent = chat_with_agent(current_agent, "Hi there!")
    print("Greeter:", response)
    
    # User wants a haiku
    response, current_agent = chat_with_agent(current_agent, "Yes, I'd love a haiku about Python!")
    print("Response:", response)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())