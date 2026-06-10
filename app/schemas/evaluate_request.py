from pydantic import BaseModel


class EvaluateRequest(BaseModel):
    question: str
    sources: list[str] = []
    answer: str
