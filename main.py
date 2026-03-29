from app.workflows.research_graph import research_graph

config = {"configurable": {"thread_id": "1"}}

initial_state = {
    "question": "What is the impact of AI on the job market?",
    "tasks": [],
    "search_results": [],
    "filtered_results": [],
    "final_answer": "",
    "iteration_count": 0 # must be initialized here — if missing, any node that does iteration_count + 1 will raise a KeyError
    # and crash the graph on first cycle since it cant increment by 1 value of absent key
    #  messages on the other hand arent initialized since add_messages handles the missing key gracefully (messages) if it will be missing
    # by treating it as an empty list and appending to it. It's defensive by design.
    # Whereas iteration_count has no reducer — LangGraph does a raw dict lookup, finds nothing, and crashes.
    # To prevent a race condition only in case the graph structure would have been paraller nodes (unlike this project case cause
    # here the nodes are sequentially and it cant happen but theoretically we shodld have done -->  iteration_count: Annotated[int, increment_reducer]  # custom reducer — safe for parallel branches
    # and add the increment_reducer looking something like :
    # def increment_reducer(current: int, update: int) -> int:
    #     return current + update

}

response = research_graph.graph.invoke(initial_state, config=config)

print("Tasks:", response["tasks"])
print("Search Results:", response["search_results"])
print("Filtered Results:", response["filtered_results"])
print("Final Answer:", response["final_answer"])
print("Iterations:", response["iteration_count"])