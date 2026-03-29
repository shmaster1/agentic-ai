import os
from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=api_key)


@tool
def perform_web_search(query: str) -> dict:
    """Search the web for information about a given query and return results with sources."""
    results = tavily_client.search(query, max_results=3)
    return results