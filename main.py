import json
import os
from openai import OpenAI

from components import AgentConfig 
from utils import load_agent_config, create_transfer_tool

# Set your OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

def chat_with_agent(agent: AgentConfig, user_message: str):
    """Chat with an agent using the OpenAI API"""
    
    messages = [
        {"role": "system", "content": agent.instructions},
        {"role": "user", "content": user_message}
    ]
    
    # Call OpenAI API
    print("Agent tools:", agent.tools)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=agent.tools if agent.tools else None,
        tool_choice="auto" if agent.tools else None,
    )
    
    assistant_message = response.choices[0].message

    print("Assistant message:", assistant_message)
    
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
                    destination_agent,
                    function_args["conversation_context"]
                )
    
    return assistant_message.content


# Example usage
async def main():
    # Start conversation with greeter agent
    response = chat_with_agent(greeter_agent, "Hi there!")
    print("Greeter:", response)
    
    # User wants a haiku
    response = chat_with_agent(greeter_agent, "Yes, I'd love a haiku about Python!")
    print("Response:", response)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())