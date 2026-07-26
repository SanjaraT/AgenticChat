import arxiv
import wikipedia
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool

from backend import config
from backend.rag_tools import rag_search

# Live web search (current events)
tavily_search = TavilySearchResults(max_results=config.TAVILY_MAX_RESULTS)

# General web search
duckduckgo_search = DuckDuckGoSearchRun(region=config.DUCKDUCKGO_REGION)


@tool
def wikipedia_search(query: str) -> str:
    """Search Wikipedia."""
    try:
        return wikipedia.summary(query, sentences=4)
    except Exception as e:
        return str(e)


@tool
def arxiv_search(query: str) -> str:
    """Search arXiv for research papers and return the top results."""
    try:
        search = arxiv.Search(
            query=query,
            max_results=config.ARXIV_MAX_RESULTS,
            sort_by=arxiv.SortCriterion.Relevance,
        )

        papers = [
            (
                f"Title: {result.title}\n"
                f"Authors: {', '.join(author.name for author in result.authors)}\n"
                f"Published: {result.published.date()}\n\n"
                f"Summary:\n{result.summary}\n\n"
                f"PDF: {result.pdf_url}"
            )
            for result in search.results()
        ]

        if not papers:
            return "No papers found."

        return ("\n\n" + "=" * 80 + "\n\n").join(papers)

    except Exception as e:
        return f"Error searching arXiv: {e}"


# Combined tool list bound to the LLM
tools = [
    tavily_search,
    duckduckgo_search,
    wikipedia_search,
    arxiv_search,
    rag_search,
]
