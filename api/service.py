from api.models import ResearchRequest, ResearchResponse
from app.workflows.research_graph import research_graph


def run_research(user_query: ResearchRequest) -> ResearchResponse:
    config = {"configurable": {"thread_id": user_query.thread_id}}

    initial_state = {
        "question": user_query.question,
        "tasks": [],
        "search_results": [],
        "filtered_results": [],
        "final_answer": "",
        "iteration_count": 0,
        "messages": []
    }

    try:
        result = research_graph.graph.invoke(initial_state, config=config)
        return ResearchResponse(**result)
    except Exception as e:
        return ResearchResponse(question=user_query.question, error=str(e))