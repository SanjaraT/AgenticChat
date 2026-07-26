from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from backend import config

embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)

vector_store = Chroma(
    persist_directory=config.VECTOR_DB_DIR,
    embedding_function=embeddings,
)

# Add document chunks to the vector store.
def add_documents(chunks) -> None:
    vector_store.add_documents(chunks)

# Return the top-k chunks most similar to the query.
def similarity_search(query: str, k: int = config.RETRIEVAL_K):
    return vector_store.similarity_search(query=query, k=k)
