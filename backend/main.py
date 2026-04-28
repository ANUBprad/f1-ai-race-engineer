from fastapi import FastAPI
from backend.schemas import StrategyInput
from backend.services import run_strategy

app = FastAPI(
    title="F1 AI Race Engineer API",
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
    return run_strategy(data)