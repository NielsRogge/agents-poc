import gradio as gr
from main import chat_with_agent
from components import AgentConfig 


def chat_wrapper(message: str, history: list[dict], agent_name: str) -> tuple[str, str]:
    response, new_agent_name = chat_with_agent(agent_name=agent_name, message=message, history=history)
    return response, new_agent_name


# Create the Gradio interface
demo = gr.ChatInterface(
    fn=chat_wrapper,
    title="Agent Chat System",
    description="Chat with our agent system. Start by saying hello!",
    additional_inputs=[
        gr.State("greeter")  # Initial agent name
    ],
    theme=gr.themes.Soft()
)

if __name__ == "__main__":
    demo.launch()