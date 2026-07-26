import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# LLM
LLM_MODEL = "llama-3.3-70b-versatile"
LLM_TEMPERATURE = 0

# Directories
UPLOAD_DIR = "uploads"
VECTOR_DB_DIR = "vector_db"
DATABASE_DIR = "database"
DATABASE_PATH = os.path.join(DATABASE_DIR, "chatbot.db")

for directory in (UPLOAD_DIR, VECTOR_DB_DIR, DATABASE_DIR):
    Path(directory).mkdir(exist_ok=True)


# RAG / Embeddings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
RETRIEVAL_K = 4

# Tools
TAVILY_MAX_RESULTS = 5
DUCKDUCKGO_REGION = "us-en"
ARXIV_MAX_RESULTS = 3
