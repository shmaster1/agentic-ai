from pydantic import BaseModel

from app.schemas.evaluation_scores import EvaluationScores


class EvaluationResponse(BaseModel):
    error: str | None = None
    scores: EvaluationScores | None = None
