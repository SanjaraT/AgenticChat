from groq import APIError
from langchain_core.messages import AIMessage
from langchain_groq import ChatGroq
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from backend import config
from backend.database import checkpointer
from backend.state import ChatState
from backend.tools import tools

# llm
llm = ChatGroq(model=config.LLM_MODEL, temperature=config.LLM_TEMPERATURE)

# tool binding
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)

# tool executer
tool_node = ToolNode(tools)

# 
def chat_node(state: ChatState):
    try:
        response = llm_with_tools.invoke(state["messages"])
    except APIError:
        response = llm.invoke(state["messages"])
        if not isinstance(response, AIMessage) or not response.content:
            response = AIMessage(
                content=(
                    "I ran into an issue trying to use a tool for that. "
                    "Could you rephrase your question or ask something simpler?"
                )
            )
    return {"messages": [response]}


def build_graph():
    graph = StateGraph(ChatState)

    graph.add_node("chat_node", chat_node)
    graph.add_node("tools", tool_node)

    graph.add_edge(START, "chat_node")
    graph.add_conditional_edges("chat_node", tools_condition)
    graph.add_edge("tools", "chat_node")

    return graph.compile(checkpointer=checkpointer)


chatbot = build_graph()
