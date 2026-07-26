"""SQLite connection and LangGraph checkpointer for conversation memory."""

import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver

from backend import config

conn = sqlite3.connect(database=config.DATABASE_PATH, check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)


def retrieve_all_threads() -> list:
    """Return a list of unique thread IDs stored in the checkpointer."""
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_threads)
