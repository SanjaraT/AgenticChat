# Sidebar
import os

import streamlit as st

from backend.rag_tools import upload_document

from ui.config import UPLOAD_DIR
from ui.state import reset_chat
from ui.utils import get_chat_title, select_thread


def render_sidebar() -> None:
    with st.sidebar:
        st.title("💬 LangGraph Chatbot")

        if st.button("➕ New Chat", use_container_width=True):
            reset_chat()

        _render_knowledge_base()
        _render_chat_list()


def _render_knowledge_base() -> None:
    st.divider()
    st.subheader("📄 Knowledge Base")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        key=f"pdf_uploader_{st.session_state['uploader_key']}",
    )

    if uploaded_file is not None:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        save_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if st.button("📥 Index Document", use_container_width=True):
            with st.spinner("Creating embeddings..."):
                try:
                    total_chunks = upload_document(save_path)
                    st.success(f"Indexed successfully! ({total_chunks} chunks)")
                    st.session_state["uploader_key"] += 1
                    st.rerun()
                except Exception as e:
                    st.error(str(e))

    if os.path.exists(UPLOAD_DIR):
        uploaded_files = os.listdir(UPLOAD_DIR)
        if uploaded_files:
            st.caption("Uploaded Documents")
            for file in uploaded_files:
                st.write("📄", file)


def _render_chat_list() -> None:
    st.divider()
    st.subheader("Chats")

    for thread_id in st.session_state["chat_threads"][::-1]:
        if st.button(
            get_chat_title(thread_id),
            use_container_width=True,
            key=str(thread_id),
        ):
            select_thread(thread_id)
