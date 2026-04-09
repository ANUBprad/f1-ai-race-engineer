import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.strategy_agent import run_strategy

# Simulation Config
TOTAL_LAPS = 10
input_data = {
    "compound": "MEDIUM",
    "tyre_age": 10,
    "circuit": "Bahrain",
    "gap_ahead": 5,
    "gap_behind": 25
}
race_history = []


# Simulation Loop
for lap in range(1, TOTAL_LAPS + 1):

    print(f"\nLAP {lap}")
    print("-" * 30)

    # Increase tyre age
    input_data["tyre_age"] += 1

    # Run strategy
    decision = run_strategy(input_data)

    # Store memory
    race_history.append({"lap": lap, "decision": decision})
    print(f"Action: {decision['action']}")
    print(f"Confidence: {decision['confidence']}")
    print(f"Reasoning: {decision['reasoning']}")

    # Simple pit logic
    if "PIT" in decision["action"]:
        print("🔧 Pit stop executed")
        input_data["tyre_age"] = 0
        input_data["compound"] = "MEDIUM"

    # Optional: simulate gap change
    input_data["gap_ahead"] = max(0, input_data["gap_ahead"] - 0.5)