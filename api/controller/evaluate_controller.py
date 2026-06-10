from fastapi import APIRouter
from starlette import status
from app.schemas.evaluate_request import EvaluateRequest
from app.schemas.evaluate_response import EvaluationResponse
from app.schemas.evaluation_scores import EvaluationScores
from app.evaluator import evaluate_response

router = APIRouter(prefix="/evaluate", tags=["evaluate"])


@router.post("/", status_code=status.HTTP_200_OK, response_model=EvaluationResponse)
def evaluate(request: EvaluateRequest):
    try:
        result = evaluate_response(request.question, request.sources, request.answer)
        return EvaluationResponse(
            scores=EvaluationScores(**{k: v for k, v in result.items() if k != "reasoning"},
                                    reasoning=result.get("reasoning", {}))
        )
    except Exception as e:
        return EvaluationResponse(error=str(e))