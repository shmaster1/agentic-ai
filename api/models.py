import uuid
from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    question: str
    thread_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

class ResearchResponse(BaseModel):
    model_config = {"extra": "ignore"}  # ignore fields not in schema e.g. "messages" which aren't meant to be sent to the user

    question: str
    tasks: list[str] = []
    search_results: list[str] = []
    filtered_results: list[str] = []
    final_answer: str = ""
    iteration_count: int = 0
    error: str | None = None  # in case nothing returns it won't be empty - only for the user side hence not in app/research_state.py
