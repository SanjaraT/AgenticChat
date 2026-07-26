import uuid

import streamlit as st

from backend.database import retrieve_all_threads


def generate_thread_id():
    return uuid.uuid4()

# Register a conversation thread if it doesn't already exist
def add_thread(thread_id) -> None:
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

# Start a new conversation with a fresh thread ID.
def reset_chat() -> None:
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(thread_id)
    st.session_state["message_history"] = []

# Initialize all Streamlit session-state keys used by the app.
def init_session_state() -> None:
    if "message_history" not in st.session_state:
        st.session_state["message_history"] = []

    if "thread_id" not in st.session_state:
        st.session_state["thread_id"] = generate_thread_id()

    if "chat_threads" not in st.session_state:
        st.session_state["chat_threads"] = retrieve_all_threads()

    if "uploader_key" not in st.session_state:
        st.session_state["uploader_key"] = 0

    add_thread(st.session_state["thread_id"])
