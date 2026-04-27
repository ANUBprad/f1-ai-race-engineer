from fastapi import FastAPI
from schemas import StrategyInput
from services import run_strategy

app = FastAPI(
    title="F1 AI Race Engineer API",
    description="Backend for F1 Strategy Simulation",
    version="1.0"
)


@app.get("/")
def home():
    return {"message": "API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/strategy")
def get_strategy(data: StrategyInput):
    result = run_strategy(data)
    return result