import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from backend.graph import chatbot


def render_chat() -> None:
    st.title("💬 LangGraph Chatbot")
    st.caption("Ask me anything.")

    for message in st.session_state["message_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Type your message...")
    if user_input:
        _handle_user_input(user_input)

# Store the user's message and stream back the assistant's reply
def _handle_user_input(user_input: str) -> None:
    st.session_state["message_history"].append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    config = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "metadata": {"thread_id": st.session_state["thread_id"]},
        "run_name": "chat_turn",
    }

    with st.chat_message("assistant"):
        tool_placeholder = st.empty()


        # Stream AI message chunks, surfacing tool usage as it happens.
        def ai_only_stream():
            for message_chunk, _metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=config,
                stream_mode="messages",
            ):
                tool_calls = getattr(message_chunk, "tool_calls", None)
                if tool_calls:
                    tool_names = [call["name"] for call in tool_calls]
                    tool_placeholder.info("🔧 Using: " + ", ".join(tool_names))

                if isinstance(message_chunk, AIMessage) and message_chunk.content:
                    yield message_chunk.content

            tool_placeholder.empty()

        ai_message = st.write_stream(ai_only_stream())

    st.session_state["message_history"].append(
        {"role": "assistant", "content": ai_message}
    )
