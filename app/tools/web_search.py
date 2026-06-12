import os
from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient

load_dotenv()


@tool
def perform_web_search(query: str) -> dict:
    """Search the web for information about a given query and return results with sources."""
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    results = client.search(query, max_results=6)

    results = tavily_client.search(query, max_results=6)
    return results