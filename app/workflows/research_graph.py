from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from app.agents.planner_agent import planner_node
from app.agents.retriever_agent import retriever_node, store_node
from app.agents.searcher_agent import searcher_node, collect_search_results
from app.agents.writer_agent import writer_node
from app.schemas.research_state import ResearchState
from app.tools.web_search import perform_web_search

MAX_ITERATIONS= 3

def should_continue(state: ResearchState) -> str:
    if state["iteration_count"] == MAX_ITERATIONS or state["final_answer"]:
        return END
    return "searcher_node"

class ResearchGraph:
    def __init__(self):
        self.graph = self._build()

    @staticmethod
    def _build():
        builder = StateGraph(ResearchState)

        # --- nodes ---
        builder.add_node("planner_node", planner_node)
        builder.add_node("searcher_node", searcher_node)
        builder.add_node("search_tools", ToolNode([perform_web_search]))
        builder.add_node("collect_results", collect_search_results)
        builder.add_node("store_node", store_node)
        builder.add_node("retriever_node", retriever_node)
        builder.add_node("writer_node", writer_node)

        # --- edges ---
        builder.add_edge(START, "planner_node")
        builder.add_edge("planner_node", "searcher_node")
        builder.add_conditional_edges("searcher_node", tools_condition,{"tools": "search_tools", END: END})
        # builder.add_edge("searcher_node", "search_tools")

        builder.add_edge("search_tools", "collect_results")
        builder.add_edge("collect_results", "store_node")
        builder.add_edge("store_node", "retriever_node")

        builder.add_edge("retriever_node", "writer_node")
        builder.add_conditional_edges("writer_node", should_continue)

        return builder.compile(checkpointer=InMemorySaver())

research_graph = ResearchGraph()
