import json
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

_eval_model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.1,
    api_key=os.getenv("GROQ_API_KEY"),
)

EVAL_PROMPT = """You are an expert evaluator for AI-generated research answers.
Score the following on 4 metrics, each from 0 to 100.

Question: {question}

Retrieved Sources:
{sources}

Final Answer:
{answer}

Metrics:
- sources: Is the final answer faithfully grounded in the provided sources? (0=hallucinated, 100=fully supported)
- coverage: Do the sources collectively cover the key aspects of the question? (0=missing most, 100=comprehensive)
- recency: How current and timely does the information in the sources appear? (0=very outdated, 100=very current)
- coherence: Is the final answer well-structured, logical, and clearly written? (0=incoherent, 100=excellent)

Respond ONLY with valid JSON, no extra text:
{{
  "sources": <0-100>,
  "coverage": <0-100>,
  "recency": <0-100>,
  "coherence": <0-100>,
  "reasoning": {{
    "sources": "<one sentence>",
    "coverage": "<one sentence>",
    "recency": "<one sentence>",
    "coherence": "<one sentence>"
  }}
}}"""


def evaluate_response(question: str, sources: list[str], answer: str) -> dict:
    sources_text = "\n".join(f"- {s}" for s in sources[:10])
    prompt = EVAL_PROMPT.format(question=question, sources=sources_text, answer=answer)
    response = _eval_model.invoke(prompt)
    content = response.content
    start = content.find("{")
    end = content.rfind("}") + 1
    return json.loads(content[start:end])


