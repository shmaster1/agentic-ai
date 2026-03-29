from fastapi import APIRouter
from starlette import status

from api import service
from api.models import ResearchRequest, ResearchResponse

router = APIRouter(
    prefix="/query",
    tags=["query"],
)

@router.post("/", status_code=status.HTTP_200_OK, response_model=ResearchResponse)
def run_research(user_query: ResearchRequest):
    return service.run_research(user_query)
