from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
import wikipedia
import arxiv


from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun
from langchain_community.utilities.arxiv import ArxivAPIWrapper
from langchain_experimental.tools.python.tool import PythonREPLTool
from dotenv import load_dotenv
import sqlite3


load_dotenv()

# Groq Model
llm = ChatGroq(
    model = "llama-3.3-70b-versatile",
    temperature=0
)

# Tools 

# Live Web Search (current events)
tavily_search = TavilySearchResults(
    max_results=5
)

# General Web Search
duckduckgo_search = DuckDuckGoSearchRun(
    region="us-en"
)

# Wikipedia
@tool
def wikipedia_search(query: str) -> str:
    """Search Wikipedia."""

    try:
        return wikipedia.summary(query, sentences=4)
    except Exception as e:
        return str(e)

# arXiv Research Papers
@tool
def arxiv_search(query: str) -> str:
    """
    Search arXiv for research papers and return the top 3 results.
    """

    try:
        search = arxiv.Search(
            query=query,
            max_results=3,
            sort_by=arxiv.SortCriterion.Relevance
        )

        papers = []

        for result in search.results():
            papers.append(
                f"""
Title: {result.title}

Authors: {', '.join(author.name for author in result.authors)}

Published: {result.published.date()}

Summary:
{result.summary}

PDF:
{result.pdf_url}
"""
            )

        if not papers:
            return "No papers found."

        return "\n\n" + "="*80 + "\n\n".join(papers)

    except Exception as e:
        return f"Error searching arXiv: {e}"


tools = [
    tavily_search,
    duckduckgo_search,
    wikipedia_search,
    arxiv_search,
]

llm_with_tools = llm.bind_tools(tools)


# States
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# define node
def chat_node(state: ChatState):
    """LLM node that may answer or request a tool call."""
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(tools)


# datbase connection
conn = sqlite3.connect(database='database/chatbot.db', check_same_thread=False)

# Checkpointer
checkpointer = SqliteSaver(conn=conn)

# Build graph
graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START,"chat_node")
graph.add_conditional_edges("chat_node",tools_condition)
graph.add_edge('tools', 'chat_node')

chatbot = graph.compile(checkpointer=checkpointer)

# retrieve unique thread ids 
def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)