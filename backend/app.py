from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .agents.orchestrator import Orchestrator

app = FastAPI(title="Agentic Insights Engine API", version="0.1.0")

# CORS for React/Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = Orchestrator()

class RunParams(BaseModel):
    sql: str | None = None
    limit: int | None = 1000

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/run")
def run_pipeline(params: RunParams = Body(...)):
    out = orchestrator.run_pipeline(params.model_dump())
    return out
