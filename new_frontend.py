import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage, AIMessage
import uuid

# =============================================================================
# Page Configuration
# =============================================================================
st.set_page_config(
    page_title="LangGraph Chatbot",
    page_icon="💬",
    layout="wide"
)

# =============================================================================
# Utility Functions
# =============================================================================

# Generate a unique thread ID for a new conversation.
def generate_thread_id():
    return uuid.uuid4()


# Add a conversation thread if it doesn't already exist.
def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


# Reset the chat by creating a new thread and clearing message history.
def reset_chat():
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(thread_id)
    st.session_state["message_history"] = []


# Load a conversation from LangGraph memory.
def load_conversation(thread_id):
    state = chatbot.get_state(
        config={"configurable": {"thread_id": thread_id}}
    )
    return state.values.get("messages", [])


# Return a readable conversation title.
def get_chat_title(thread_id):
    messages = load_conversation(thread_id)

    for msg in messages:
        if isinstance(msg, HumanMessage):
            title = msg.content.strip()
            return title[:35] + "..." if len(title) > 35 else title

    return "New Chat"


# =============================================================================
# Session State
# =============================================================================

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = []

add_thread(st.session_state["thread_id"])

# =============================================================================
# Sidebar
# =============================================================================

with st.sidebar:

    st.title("💬 LangGraph Chatbot")

    if st.button("➕ New Chat", use_container_width=True):
        reset_chat()

    st.divider()
    st.subheader("Chats")

    for thread_id in st.session_state["chat_threads"][::-1]:

        if st.button(
            get_chat_title(thread_id),
            use_container_width=True,
            key=str(thread_id)
        ):

            st.session_state["thread_id"] = thread_id

            messages = load_conversation(thread_id)

            temp_messages = []

            for msg in messages:

                role = (
                    "user"
                    if isinstance(msg, HumanMessage)
                    else "assistant"
                )

                temp_messages.append(
                    {
                        "role": role,
                        "content": msg.content,
                    }
                )

            st.session_state["message_history"] = temp_messages

# =============================================================================
# Main Interface
# =============================================================================

st.title("💬 LangGraph Chatbot")
st.caption("Ask me anything.")

# Display previous conversation
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Type your message...")

if user_input:

    # Store user message
    st.session_state["message_history"].append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    CONFIG = {
        "configurable": {
            "thread_id": st.session_state["thread_id"]
        }
    }

    with st.chat_message("assistant"):

        # Stream only AI responses.
        def ai_only_stream():

            for message_chunk, metadata in chatbot.stream(
                {
                    "messages": [
                        HumanMessage(content=user_input)
                    ]
                },
                config=CONFIG,
                stream_mode="messages",
            ):

                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content

        ai_message = st.write_stream(ai_only_stream())

    # Store assistant response
    st.session_state["message_history"].append(
        {
            "role": "assistant",
            "content": ai_message,
        }
    )