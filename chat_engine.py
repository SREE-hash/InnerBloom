import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Load environment variables
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found. Please check your .env file")

# Initialize the LLM (via OpenRouter API)
llm = ChatOpenAI(
    openai_api_key=OPENROUTER_API_KEY,
    temperature=0.7,
    model="mistralai/mistral-7b-instruct:free",  # auto-selects a good free model
    openai_api_base="https://openrouter.ai/api/v1"
)

# Store per-user memory sessions
session_memory_map = {}


def get_response(session_id: str, user_query: str) -> str:
    """Get chatbot response with per-session memory, safe error handling."""
    try:
        print(f"[DEBUG] New query received. session_id={session_id}, user_query={user_query}")

        if session_id not in session_memory_map:
            print("[DEBUG] Creating new session with memory")
            memory = ConversationBufferMemory(return_messages=True)
            session_memory_map[session_id] = ConversationChain(
                llm=llm,
                memory=memory,
                verbose=True
            )

        conversation = session_memory_map[session_id]
        response = conversation.predict(input=user_query)
        print(f"[DEBUG] LLM Response: {response}")

        return response

    except Exception as e:
        import traceback
        print("[ERROR] Exception in get_response:", str(e))
        traceback.print_exc()
        return "⚠️ Sorry, something went wrong while generating a response. Please try again."
