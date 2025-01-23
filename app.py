import gradio as gr
from main import chat_with_agent
from components import Agent
from utils import create_transfer_tool

from agents import authentication_agent, returns_agent, sales_agent, simulated_human_agent


def chat_wrapper(
    message: str, history: list[dict], agent: Agent
) -> tuple[str, Agent]:
    # Create a new instance of the agent for each chat interaction
    # This prevents circular reference issues
    current_agent = Agent(
        name=agent.name,
        public_description=agent.public_description,
        instructions=agent.instructions,
        tools=agent.tools,
        tool_logic=agent.tool_logic
    )
    
    response, new_agent = chat_with_agent(
        agent=current_agent, message=message, history=history
    )
    return response, new_agent


# Define downstream agents without circular references
all_agents = [authentication_agent, returns_agent, sales_agent, simulated_human_agent]

# Add transfer tools without creating circular references
for agent in all_agents:
    other_agents = [a for a in all_agents if a != agent]
    tool = create_transfer_tool(other_agents)
    agent.tools.append(tool)

with gr.Blocks() as demo:
    session_id = gr.State(value=authentication_agent)
    gr.ChatInterface(
        fn=chat_wrapper,
        chatbot=gr.Chatbot(height=600, type="messages"),
        type="messages",
        title="Multi-Agent Chat System",
        description="Chat with our multi-agent system. Start by saying hello!",
        additional_inputs=[session_id],
        additional_outputs=[session_id],
        theme=gr.themes.Soft(),
    )

if __name__ == "__main__":
    demo.launch()
