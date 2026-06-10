from fastapi import FastAPI
from api.controller.research_controller import router as research_router
from api.controller.evaluate_controller import router as evaluate_router

app = FastAPI(
    title="ResearchNexus",
    description="Autonomous Multi-Agent Research Assistant",
    version="1.0.0"
)

app.include_router(research_router)
app.include_router(evaluate_router)


@app.get("/health")
def health():
    return {"status": "ok"}