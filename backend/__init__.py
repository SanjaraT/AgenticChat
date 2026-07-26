"""
Backend package.

Public API used by the frontend:
- chatbot: compiled LangGraph chat graph with tools + checkpointing
- retrieve_all_threads: list all saved conversation thread IDs
- upload_document: index a PDF file into the RAG vector store
"""

from .database import retrieve_all_threads
from .graph import chatbot
from .rag_tools import upload_document

__all__ = ["chatbot", "retrieve_all_threads", "upload_document"]
