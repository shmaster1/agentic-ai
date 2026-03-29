from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages


class ResearchState(TypedDict):
    question: str                    # user input
    tasks: list[str]                 # planner output
    search_results: list[str]        # search agent output
    filtered_results: list[str]      # retriever output
    final_answer: str                # writer output
    iteration_count: int             # tracks cycles for the loop
    messages: Annotated[list[AnyMessage], add_messages] # annotated tells LangGraph to use add_messages as a reducer cause
    # message must be appended itt must be here since if not the last message will always overriden letting the
    # next node in the turn to see only the last msg instead of all the accumulative messages meaning losing message history.

    # AnyMessage accepts any message type: HumanMessage, SystemMessage, AIMessage, ToolMessage

    # other fields behavior is overwrite  -> last write wins. That's intentional for fields like tasks and iteration_count
    # because each node owns its field completely and the previous value is no longer needed once the next node updates it.

