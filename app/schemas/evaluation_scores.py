from pydantic import BaseModel


class EvaluationScores(BaseModel):
    sources: int
    coverage: int
    recency: int
    coherence: int
    reasoning: dict[str, str] = {}