import os
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Import your modules
from model import chatRequest   # make sure this has session_id & query fields
from chat_engine import get_response

from logger import log_chat


# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Enable CORS so Streamlit can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # in dev: allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI-powered Mental Health chatbot **InnerBloom**!"}

@app.post("/chat")
def chat_with_memory(request: chatRequest):
    session_id = request.session_id
    user_query = request.query
    
    
    
    # Normal LLM response
    response = get_response(session_id, user_query)
        # Handle None safely
    if not response:
        response = "⚠️ Sorry, I couldn’t generate a response right now. Please try again."

    # Log the chat
    log_chat(session_id, user_query, response)
    return {"response": response}


    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
 