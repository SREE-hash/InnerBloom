import streamlit as st
import requests
import uuid

st.set_page_config(page_title="InnerBloom Chatbot", page_icon="💬", layout="centered")

st.title("💬 InnerBloom - AI Powered Mental Health Companion Chatbot")

# Generate a unique session_id per user session
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_bot_response(message):
    url = "https://innerbloom-2.onrender.com"  # FastAPI backend URL
    payload = {
        "session_id": st.session_state.session_id,
        "query": message
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("response", "⚠️ No response field in backend reply")
    except Exception as e:
        return f"⚠️ Error: {e}"

# Chat input
if user_input := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    bot_reply = get_bot_response(user_input)
    st.session_state.messages.append({"role": "bot", "content": bot_reply})

# Display chat
for msg in st.session_state.messages:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])

