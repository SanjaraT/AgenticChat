from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend import config

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=config.CHUNK_SIZE,
    chunk_overlap=config.CHUNK_OVERLAP,
)


def split_documents(documents):
    return text_splitter.split_documents(documents)
