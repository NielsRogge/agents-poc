import json
import os
import openai

from components import AgentConfig, create_transfer_tool
from utils import load_agent_config

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load agent configurations
haiku_config = load_agent_config('haiku.txt')
haiku_agent = AgentConfig(
    name=haiku_config['name'],
    public_description=haiku_config['description'],
    instructions=haiku_config['instructions'],
    tools=[],
)

greeter_config = load_agent_config('greeter.txt')
greeter_agent = AgentConfig(
    name=greeter_config['name'],
    public_description=greeter_config['description'],
    instructions=greeter_config['instructions'],
    tools=[],
    downstream_agents=[haiku_agent]
)

# Add transfer tool to greeter
greeter_agent.tools.append(create_transfer_tool(greeter_agent.downstream_agents))

async def chat_with_agent(agent: AgentConfig, user_message: str):
    """Chat with an agent using the OpenAI API"""
    
    messages = [
        {"role": "system", "content": agent.instructions},
        {"role": "user", "content": user_message}
    ]
    
    # Call OpenAI API
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=messages,
        functions=agent.tools if agent.tools else None,
        function_call="auto"
    )
    
    assistant_message = response.choices[0].message
    
    # Handle function calls
    if assistant_message.get("function_call"):
        function_name = assistant_message["function_call"]["name"]
        function_args = json.loads(assistant_message["function_call"]["arguments"])
        
        if function_name == "transferAgents":
            # Find the destination agent
            destination_agent = next(
                (agent for agent in agent.downstream_agents 
                 if agent.name == function_args["destination_agent"]),
                None
            )
            if destination_agent:
                print(f"Transferring to {destination_agent.name}...")
                return await chat_with_agent(
                    destination_agent,
                    function_args["conversation_context"]
                )
    
    return assistant_message["content"]


# Example usage
async def main():
    # Start conversation with greeter agent
    response = await chat_with_agent(greeter_agent, "Hi there!")
    print("Greeter:", response)
    
    # User wants a haiku
    response = await chat_with_agent(greeter_agent, "Yes, I'd love a haiku about Python!")
    print("Response:", response)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())