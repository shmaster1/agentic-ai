from pydantic import BaseModel
from typing import List

# Pydantic models enforce structure at the agent level only
# they are NOT part of ResearchState which is the graph-level shared state

class PlannerOutput(BaseModel):
    tasks: List[str]
    reasoning: str                  # why it broke it down this way

class SearchOutput(BaseModel):
    search_results: List[str]
    queries_used: List[str]         # what queries were sent to Tavily

class RetrieverOutput(BaseModel):
    filtered_results: List[str]
    relevance_scores: List[float]   # how relevant each result is

class WriterOutput(BaseModel):
    final_answer: str
    sources: List[str]              # cited sources