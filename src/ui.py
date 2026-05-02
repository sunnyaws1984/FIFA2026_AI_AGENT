"""
ui.py — Gradio frontend for FIFA 2026 ADK Agent
Run: python ui.py
URL: http://localhost:7860
"""

import asyncio
from dotenv import load_dotenv
load_dotenv()

import gradio as gr
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.errors.already_exists_error import AlreadyExistsError
from google.genai import types
from agent import root_agent

# ── ADK Setup ──────────────────────────────────────────────────────────────
SESSION_SERVICE = InMemorySessionService()
RUNNER          = Runner(
                    agent=root_agent,
                    app_name="fifa2026_app",
                    session_service=SESSION_SERVICE,
                  )
APP_NAME   = "fifa2026_app"
USER_ID    = "student_user"
SESSION_ID = "fifa2026_session"


async def init_session():
    try:
        await SESSION_SERVICE.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID,
        )
    except AlreadyExistsError:
        pass  # session already exists — reuse it


async def ask_agent(question: str) -> str:
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
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text

    return final_response or "No response from agent."


def chat(user_message: str, history):
    asyncio.run(init_session())
    response = asyncio.run(ask_agent(user_message))
    return response                    # ✅ gr.ChatInterface only needs the response string


demo = gr.ChatInterface(
    fn=chat,
    title="⚽ FIFA 2026 Agent",
    description="Ask me anything about FIFA 2026 venues, teams and matches."
)

if __name__ == "__main__":
    print("✅ Starting FIFA 2026 Agent...")
    print("🌐 Open: http://localhost:7860")
    demo.launch(server_name="0.0.0.0", server_port=7860)