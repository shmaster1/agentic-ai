from fastapi import FastAPI
from api.controller import router as research_router


app = FastAPI(
    title="ResearchNexus",
    description="Autonomous Multi-Agent Research Assistant",
    version="1.0.0"
)

app.include_router(research_router)


@app.get("/health")
def health():
    return {"status": "ok"}