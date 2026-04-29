from fastapi import FastAPI
from backend.schemas import StrategyInput
from backend.services import run_strategy, run_simulation
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="F1 AI Race Engineer API",
    version="1.0"
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


@app.post("/simulate")
def simulate(data: StrategyInput):
    return run_simulation(data)