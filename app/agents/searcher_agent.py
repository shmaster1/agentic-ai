import json
from langchain_core.messages import SystemMessage, HumanMessage
from app.models.llm import search_model_with_tools
from app.prompts.searcher_prompt import SEARCHER_PROMPT
from app.schemas.research_state import ResearchState


def searcher_node(state: ResearchState) -> dict:
    tasks = '\n\n'.join(state["tasks"])
    previous_answer = state.get("final_answer", "")
    content = f"Tasks:\n{tasks}"
    if previous_answer:
        content += f"\n\nPrevious answer (improve upon this):\n{previous_answer}"
    messages = [SystemMessage(content=SEARCHER_PROMPT), HumanMessage(content=content)]
    results = search_model_with_tools.invoke(messages)
    return {
        "messages": [results],  # ← store AIMessage so ToolNode can read tool calls
    }

def collect_search_results(state: ResearchState) -> dict:
    tool_messages = [m for m in state["messages"] if type(m).__name__ == "ToolMessage"]
    results = []
    for msg in tool_messages:
        try:
            parsed = json.loads(msg.content)
            for result in parsed.get("results", []):
                results.append(f"{result['title']} - {result['url']}\n{result['content']}")
        except (json.JSONDecodeError, KeyError):
            results.extend([r for r in msg.content.split('\n') if r.strip()])
    return {"search_results": results}
