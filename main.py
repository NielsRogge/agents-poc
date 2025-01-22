import json
import os
from openai import OpenAI

from components import Agent 
from utils import create_transfer_tool, get_agent

# Set your OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def chat_with_agent(agent: Agent, message: str, history: list[dict]) -> tuple[str, Agent]:
    """Chat with an agent using the OpenAI API"""
    
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
    
    return assistant_message.content, agent


# Example usage
def main():
    # Load agents
    greeter_agent = get_agent("greeter")
    haiku_agent = get_agent("haiku")
    greeter_agent.downstream_agents = [haiku_agent]
    tool = create_transfer_tool(greeter_agent.downstream_agents)
    greeter_agent.tools.append(tool)
    
    # Start conversation with greeter agent
    response, _ = chat_with_agent(greeter_agent, "Hi there!", history=[])
    print("Greeter:", response)
    
    # Start conversation with haiku agent
    response, _ = chat_with_agent(haiku_agent, "Yes, I'd love a haiku about Python!", history=[])
    print("Haiku:", response)


if __name__ == "__main__":
    main()