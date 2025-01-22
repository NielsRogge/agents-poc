import gradio as gr
from main import chat_with_agent
from components import Agent 
from utils import get_agent, create_transfer_tool


def chat_wrapper(message: str, history: list[dict], agent: Agent) -> tuple[str, Agent]:
    
    response, new_agent = chat_with_agent(agent=agent, message=message, history=history)
    return response, new_agent


greeter_agent = get_agent("greeter")
haiku_agent = get_agent("haiku")
greeter_agent.downstream_agents = [haiku_agent]
tool = create_transfer_tool(greeter_agent.downstream_agents)
greeter_agent.tools.append(tool)
agent = greeter_agent


with gr.Blocks() as demo:
    session_id = gr.State(value=agent)
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