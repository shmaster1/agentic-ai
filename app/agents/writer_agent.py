from langchain_core.messages import SystemMessage, HumanMessage

from app.models.llm import writer_model
from app.prompts.writer_prompt import WRITER_PROMPT
from app.schemas.research_state import ResearchState


def writer_node(state: ResearchState) -> dict:
    filtered_results = '\n\n'.join(state["filtered_results"])
    messages = [
        SystemMessage(content=WRITER_PROMPT),
        HumanMessage(content=f"Question: {state['question']}\n\nFiltered Results:\n{filtered_results}")
    ]
    final_results = writer_model.invoke(messages)
    state["iteration_count"] += 1
    return {
        "final_answer": final_results.content,
        "iteration_count": state["iteration_count"] + 1
    }