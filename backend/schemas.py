from pydantic import BaseModel

class StrategyInput(BaseModel):
    compound: str
    tyre_age: int
    circuit: str
    gap_ahead: float
    gap_behind: float