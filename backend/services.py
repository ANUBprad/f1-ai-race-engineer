import sys
import os
sys.path.append(os.path.abspath(".."))

from ml.strategy_engine import StrategyEngine

engine = StrategyEngine()


def run_strategy(data):
    result = engine.decide(
        compound=data.compound,
        tyre_age=data.tyre_age,
        circuit=data.circuit,
        gap_ahead=data.gap_ahead,
        gap_behind=data.gap_behind
    )
    return result