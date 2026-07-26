from pathlib import Path

from langchain_core.tools import tool

from backend.loader import load_pdf
from backend.splitter import split_documents
from backend.vector_store import add_documents, similarity_search

# Load  PDF --> split it into chunks --> tag it with its source filename --> store it in the vector database --> Returns the number of chunks indexed
def upload_document(file_path: str) -> int:
    documents = load_pdf(file_path)
    chunks = split_documents(documents)

    filename = Path(file_path).name
    for chunk in chunks:
        chunk.metadata["source"] = filename

    add_documents(chunks)
    return len(chunks)

# Return the top-k most relevant document chunks for a query
def retrieve_documents(query: str, k: int = 4):
    return similarity_search(query, k=k)


@tool
def rag_search(question: str) -> str:
    """
    Search uploaded documents.

    Use this tool ONLY if the user asks questions about uploaded
    PDFs, reports, books, lecture slides, or documents.
    """
    docs = retrieve_documents(question)

    if not docs:
        return "No uploaded documents found."

    context = []
    for doc in docs:
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "-")
        context.append(
            f"Source: {source}\nPage: {page}\n\nContent:\n{doc.page_content}"
        )

    return "\n\n------------------------\n\n".join(context)
