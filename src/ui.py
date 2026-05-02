"""
ui.py
-----
Gradio frontend for the FIFA 2026 ADK agent.
Run with:  python ui.py
Opens at:  http://localhost:7860
"""

import asyncio
import gradio as gr

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent import root_agent

# ── ADK Runner Setup ───────────────────────────────────────────────────────
SESSION_SERVICE = InMemorySessionService()

RUNNER = Runner(
    agent=root_agent,
    app_name="fifa2026_app",
    session_service=SESSION_SERVICE,
)

# Fixed session for the UI (one session per browser session is fine for demo)
APP_NAME    = "fifa2026_app"
USER_ID     = "student_user"
SESSION_ID  = "fifa2026_session"


async def init_session():
    """Create a session if it doesn't exist yet."""
    await SESSION_SERVICE.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )


async def ask_agent(question: str) -> str:
    """Send a question to the ADK agent and return its response."""
    message = types.Content(
        role="user",
        parts=[types.Part(text=question)]
    )

    final_response = ""

    async for event in RUNNER.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=message,
    ):
        # Capture the final text response from the agent
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text

    return final_response or "No response from agent."


def chat(user_message: str, history: list):
    """Gradio chat handler — runs the async agent call."""
    asyncio.run(init_session())
    response = asyncio.run(ask_agent(user_message))
    history.append((user_message, response))
    return "", history


# ── Gradio UI ──────────────────────────────────────────────────────────────
with gr.Blocks(title="FIFA 2026 Agent", theme=gr.themes.Soft()) as demo:

    gr.Markdown("# FIFA 2026 Agent")
    gr.Markdown("Ask any question about FIFA 2026 venues, teams, and matches.")

    chatbot = gr.Chatbot(height=450, label="FIFA 2026 Q&A")
    msg     = gr.Textbox(placeholder="e.g. Which teams are in Group A?", label="Your question")
    send    = gr.Button("Ask", variant="primary")
    clear   = gr.Button("Clear")

    # Example questions students can click
    gr.Examples(
        examples=[
            "What venues are in the USA?",
            "Which teams are in Group A?",
            "Tell me about the Final match.",
            "Show me all matches involving Brazil.",
            "How many venues are in Mexico?",
            "List all teams in the tournament.",
        ],
        inputs=msg,
    )

    # Event handlers
    send.click(chat, inputs=[msg, chatbot], outputs=[msg, chatbot])
    msg.submit(chat, inputs=[msg, chatbot], outputs=[msg, chatbot])
    clear.click(lambda: [], outputs=chatbot)


# ── Entry point ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Starting FIFA 2026 Agent UI...")
    print("Open: http://localhost:7860")
    demo.launch(server_name="0.0.0.0", server_port=7860)
