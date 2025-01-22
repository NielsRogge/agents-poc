import gradio as gr
from main import chat_with_agent


# Create the Gradio interface
demo = gr.ChatInterface(
    fn=chat_with_agent,
    title="Agent Chat System",
    additional_outputs=[
        gr.outputs.Textbox(label="Current Agent"),
    ],
    description="Chat with our agent system. Start by saying hello!",
    examples=["Hi there!", "I'd like a haiku about Python", "Can you write a haiku about nature?"],
    theme=gr.themes.Soft()
)

demo.launch()