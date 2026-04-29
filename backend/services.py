import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

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

    return {
        "action": result["action"],
        "confidence": float(result["confidence"]),
        "reasoning": result.get("reasoning", "")
    }

def run_simulation(data):
    try:
        stay_loss = engine.simulate_stay_out(data.compound, data.tyre_age)
        pit_loss = engine.simulate_pit(data.circuit)

        # simulate_undercut returns boolean → don't round
        undercut_possible = engine.simulate_undercut(
            data.compound,
            data.tyre_age,
            data.gap_ahead
        )

        return {
            "stay_out_loss": round(float(stay_loss), 2),
            "pit_loss": round(float(pit_loss), 2),
            "undercut_possible": bool(undercut_possible)
        }

    except Exception as e:
        print("SIMULATION ERROR:", e)
        return {
            "error": str(e)
        }