import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from app.tools.web_search import perform_web_search

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

def get_model(temperature: float = 0.5) -> ChatGroq:
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=temperature,
        api_key=api_key
    )

planner_model = get_model(temperature=0.3)   # precise, structured thinking
search_model = get_model(temperature=0.1)    # factual, no creativity
search_model_with_tools = search_model.bind_tools([perform_web_search]) # This way binding happens once at startup, not on every node call.
retriever_model = get_model(temperature=0.1) # factual, ranking based
writer_model = get_model(temperature=0.7)    # creative, fluent writing