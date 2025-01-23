import json
import os
from openai import OpenAI

from agents import greeter_agent, haiku_agent

from components import Agent
from utils import create_transfer_tool

# Set your OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def chat_with_agent(
    agent: Agent, message: str, history: list[dict]
) -> tuple[str, Agent]:
    """Chat with an agent using the OpenAI API"""

    messages = [{"role": "system", "content": agent.instructions}]
    for history_message in history:
        messages.append(
            {
                "role": history_message["role"],
                "content": history_message["content"],
            }
        )
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

        print(f"Function name: {function_name}")
        print(f"Function args: {function_args}")

        if function_name == "transferAgents":
            # Find the destination agent
            destination_agent = next(
                (
                    agent
                    for agent in agent.downstream_agents
                    if agent.name == function_args["destination_agent"]
                ),
                None,
            )
            if destination_agent:
                print(f"Transferring to {destination_agent.name}...")
                return chat_with_agent(
                    agent=destination_agent,
                    message=function_args["conversation_context"],
                    history=history,
                )
        
        # Execute tool logic if available
        elif function_name in agent.tool_logic:
            tool_result = agent.tool_logic[function_name](
                function_args, 
                history
            )
            
            # Add tool result to conversation
            messages.append({
                "role": "function",
                "name": function_name,
                "content": json.dumps(tool_result)
            })
            
            # Get final response from agent
            final_response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            return final_response.choices[0].message.content, agent

    return assistant_message.content, agent


# Example usage
def main():
    # Load agents
    greeter_agent.downstream_agents = [haiku_agent]
    tool = create_transfer_tool(greeter_agent.downstream_agents)
    greeter_agent.tools.append(tool)

    # Start conversation with greeter agent
    response, _ = chat_with_agent(greeter_agent, "Hi there!", history=[])
    print("Greeter:", response)

    # Start conversation with haiku agent
    response, _ = chat_with_agent(
        haiku_agent, "Yes, I'd love a haiku about Python!", history=[]
    )
    print("Haiku:", response)


if __name__ == "__main__":
    main()
