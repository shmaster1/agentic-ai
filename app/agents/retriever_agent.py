from app.schemas.research_state import ResearchState
from app.tools.vector_store import store_results, fetch_relevant_results


def store_node(state: ResearchState) -> dict:
    # join all search results into one string and store in vector db
    # side effect only — no state update needed
    all_results = '\n\n'.join(state["search_results"])
    store_results.invoke({"results": all_results})
    return {}

def retriever_node(state: ResearchState) -> dict:
    # fetch relevant chunks from vector store using embedding similarity
    # deterministic — no LLM needed, near_vector handles scoring
    results = fetch_relevant_results.invoke({"query": state["question"]})
    return {"filtered_results": results}
