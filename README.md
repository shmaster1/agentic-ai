# ResearchNexus — Autonomous Multi-Agent Research Assistant

> A production-grade multi-agent research system built with LangGraph, FastAPI, and Streamlit. Given a complex research question, ResearchNexus autonomously breaks it down into sub-tasks, searches the web, filters and ranks results, and compiles a structured research report — all observable in real time.

---

## Architecture

```
User Question
      ↓
┌─────────────┐
│Planner Agent│  Breaks question into 3-6 focused sub-tasks
└──────┬──────┘
       ↓
┌─────────────┐
│Search Agent │  Executes Tavily web search per sub-task
└──────┬──────┘
       ↓
┌───────────────┐
│Retriever Agent│  Embeds results → stores in Weaviate → fetches most relevant chunks
└──────┬────────┘
       ↓
┌─────────────┐
│Writer Agent │  Compiles structured research report with citations
└──────┬──────┘
       ↓
  Complete? ──→ END
  Incomplete? ──→ loop back to Search (max 3 iterations)
```

Each agent has its own:
- LLM instance with tuned temperature
- Custom system prompt
- Dedicated tools (where applicable)
- Pydantic output schema for validation

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent Orchestration | LangGraph `StateGraph` with cyclic iteration |
| LLM | Groq `llama-3.3-70b-versatile` |
| Web Search | Tavily API |
| Vector Store | Weaviate (Docker) + Sentence Transformers embeddings |
| Backend | FastAPI + Uvicorn |
| Frontend | Streamlit with per-agent checkpoint visualization |
| State Management | LangGraph `InMemorySaver` checkpointer |

---

## Key Concepts Demonstrated

- **Multi-agent orchestration** — 4 specialized agents with distinct roles wired via LangGraph `StateGraph`
- **Cyclic iteration** — conditional edges loop back to Search if results are incomplete
- **Hybrid state schema** — `TypedDict` for graph state, Pydantic `BaseModel` for per-agent output validation
- **RAG pipeline** — Tavily results chunked, embedded via Sentence Transformers, stored and queried from Weaviate
- **Observable UI** — Streamlit dashboard showing per-agent input/output at each checkpoint
- **Layered architecture** — Model / Controller / View separation (LangGraph / FastAPI / Streamlit)

---

## Project Structure

```
researchnexus/
│
├── app/
│   ├── agents/
│   │   ├── planner_agent.py
│   │   ├── searcher_agent.py
│   │   ├── retriever_agent.py
│   │   └── writer_agent.py
│   │
│   ├── workflows/
│   │   └── research_graph.py    # StateGraph — wires all 4 agents
│   │
│   ├── tools/
│   │   ├── web_search.py        # Tavily search tool
│   │   └── vector_store.py      # Weaviate store + fetch tools
│   │
│   ├── prompts/                 # Custom system prompt per agent
│   ├── schemas/
│   │   ├── research_state.py    # TypedDict shared graph state
│   │   └── outputs.py           # Pydantic output schemas per agent
│   └── models/
│       └── llm.py               # ChatGroq instances per agent
│
├── api/
│   ├── controller.py            # FastAPI router
│   ├── service.py               # Graph invocation layer
│   ├── models.py                # Request / Response Pydantic models
│   └── main.py                  # FastAPI app entry point
│
├── ui/
│   └── streamlit_app.py         # Observable agent dashboard
│
├── docker-compose.yml           # Weaviate local instance
├── requirements.txt
└── .env.example
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/researchnexus.git
cd researchnexus
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
```

Fill in your `.env`:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
WEAVIATE_URL=http://localhost:8082
```

### 5. Start Weaviate

```bash
docker-compose up -d
```

### 6. Start the FastAPI backend

```bash
PYTHONPATH=. .venv/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### 7. Start the Streamlit UI

```bash
streamlit run ui/streamlit_app.py
```

Open `http://localhost:8501` in your browser.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/query/` | Run a research query through the full agent pipeline |
| `GET` | `/health` | Health check |
| `GET` | `/docs` | Interactive Swagger UI |

### Example request

```bash
curl -X POST http://localhost:8000/query/ \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the impact of AI on the job market?", "thread_id": "1"}'
```

---

## Free API Keys

| Service | Sign up | Free tier |
|---------|---------|-----------|
| Groq | console.groq.com | Generous free tier |
| Tavily | app.tavily.com | 1,000 searches/month |

---

## Roadmap

- [ ] SSE streaming — real-time agent updates in the UI
- [ ] Persistent checkpointer — PostgreSQL instead of InMemorySaver
- [ ] LangSmith tracing — full observability and evaluation
- [ ] Docker Compose full stack — single command startup
- [ ] Unit tests per agent

---

## Learning Path

This project was built incrementally across 3 phases:

| Phase | Focus | Key concepts |
|-------|-------|-------------|
| 1 | Single agent | `@tool`, `create_agent`, structured output, memory |
| 2 | StateGraph migration | `TypedDict` state, nodes, edges, `ToolNode` |
| 3 | Multi-agent system | 4 agents, cyclic iteration, RAG, FastAPI, Streamlit |