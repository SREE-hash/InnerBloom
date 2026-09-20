
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY not found. Please check your .env file."
    )

# OpenRouter free model router
llm = ChatOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    model="openrouter/free",
    temperature=0.7,
)

# Store conversation history for each session
session_memory_map = {}


def get_response(session_id: str, user_query: str) -> str:
    """Generate an InnerBloom response with per-session memory."""

    try:
        print(
            f"[DEBUG] New query received. "
            f"session_id={session_id}, user_query={user_query}"
        )

        # Create a new conversation history for a new session
        if session_id not in session_memory_map:
            print("[DEBUG] Creating new session with memory")
            session_memory_map[session_id] = []

        conversation_history = session_memory_map[session_id]

        # Build messages for the model
        messages = [
            (
                "system",
                """You are InnerBloom, a supportive AI mental health companion.

Your role is to:
- Listen empathetically.
- Respond in a calm, respectful and non-judgmental way.
- Help users think through everyday stress, anxiety, studies,
  relationships and emotional difficulties.
- Suggest practical and healthy coping strategies.

Important:
- You are not a doctor, therapist, or emergency service.
- Do not diagnose mental health conditions.
- Do not claim to provide professional medical treatment.
- If someone appears to be in immediate danger or may hurt themselves,
  encourage them to contact local emergency services, a trusted person,
  or a qualified mental-health professional immediately.
"""
            )
        ]

        # Add previous conversation
        messages.extend(conversation_history)

        # Add current user message
        messages.append(("human", user_query))

        # Generate response through OpenRouter
        result = llm.invoke(messages)

        response = result.content

        if not response:
            response = (
                "I'm sorry, I couldn't generate a response right now. "
                "Please try again."
            )

        # Save conversation
        conversation_history.append(("human", user_query))
        conversation_history.append(("ai", response))

        print(f"[DEBUG] LLM Response: {response}")

        return response

    except Exception as e:
        import traceback

        print("[ERROR] Exception in get_response:", str(e))
        traceback.print_exc()

        return [(
            "⚠️ Sorry, something went wrong while generating "
            "a response. Please try again later."
        )]

