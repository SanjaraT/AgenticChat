# Helpers for loading, titling, and switching between conversation threads

import streamlit as st
from langchain_core.messages import HumanMessage

from backend.graph import chatbot

# Load a conversation's messages from LangGraph memory
def load_conversation(thread_id):
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    return state.values.get("messages", [])

# Return a readable conversation title based on the first user message.
def get_chat_title(thread_id) -> str:
    messages = load_conversation(thread_id)

    for msg in messages:
        if isinstance(msg, HumanMessage):
            title = msg.content.strip()
            return title[:35] + "..." if len(title) > 35 else title

    return "New Chat"

# Switch the active thread and load its history into session state.
def select_thread(thread_id) -> None:
    st.session_state["thread_id"] = thread_id
    messages = load_conversation(thread_id)

    st.session_state["message_history"] = [
        {
            "role": "user" if isinstance(msg, HumanMessage) else "assistant",
            "content": msg.content,
        }
        for msg in messages
    ]
