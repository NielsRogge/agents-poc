import gradio as gr
from main import chat_with_agent
from components import Agent 
from utils import create_transfer_tool


def chat_wrapper(message: str, history: list[dict], agent: Agent) -> tuple[str, Agent]:
    
    if agent is None:
        agent = get_agent("greeter")
        agent.tools.append(create_transfer_tool(agent.downstream_agents))
    
    response, new_agent = chat_with_agent(agent=agent, message=message, history=history)
    return response, new_agent


with gr.Blocks() as demo:
    session_id = gr.State()
    demo = gr.ChatInterface(
        fn=chat_wrapper,
        title="Agent Chat System",
        description="Chat with our agent system. Start by saying hello!",
        additional_inputs=[session_id],
        additional_outputs=[session_id],
        theme=gr.themes.Soft()
    )

if __name__ == "__main__":
    demo.launch()