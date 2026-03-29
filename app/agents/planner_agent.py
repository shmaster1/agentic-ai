from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import ValidationError
import json
import re
from app.models.llm import planner_model
from app.prompts.planner_prompt import PLANNER_PROMPT
from app.schemas.outoput import PlannerOutput
from app.schemas.research_state import ResearchState


def planner_node(state: ResearchState) -> dict:
    messages = [SystemMessage(content=PLANNER_PROMPT), HumanMessage(content=state["question"])]
    results = planner_model.invoke(messages)

    try:
        # strip markdown backticks if LLM ignores the prompt instruction
        extracted_json_string = re.sub(r'```json|```', '', results.content).strip()
        # parse JSON — more robust than startswith() string splitting
        parsed = json.loads(extracted_json_string)
        validated_tasks = parsed.get("tasks", [])
        validated_reasoning = parsed.get("reasoning", "")

        # PlannerOutput construction triggers Pydantic validation
        # field_validator on tasks will raise ValidationError if list is empty
        validated = PlannerOutput(tasks=validated_tasks, reasoning=validated_reasoning)
        # return only what ResearchState expects — reasoning lives at agent level only
        return {"tasks": validated.tasks}

    except (ValueError, json.JSONDecodeError, ValidationError) as e:
        raise ValueError(f"Planner node failed: {e}") from e