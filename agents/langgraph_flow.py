import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import TypedDict
from langgraph.graph import StateGraph, END
from agents.strategy_agent import run_strategy
from agents.analyst_agent import analyze_decision


# STATE DEFINITION
class AgentState(TypedDict):
    input_data: dict
    strategy_output: dict
    final_output: dict


# =========================
# NODES
# =========================

# Strategy Node
def strategy_node(state: AgentState):
    input_data = state.get("input_data")
    decision = run_strategy(input_data)

    return {
        "input_data": input_data,
        "strategy_output": decision
    }


# Analyst Node
def analyst_node(state: AgentState):
    input_data = state.get("input_data")
    strategy_output = state.get("strategy_output")

    final = analyze_decision(input_data, strategy_output)

    return {
        "input_data": input_data,
        "strategy_output": strategy_output,
        "final_output": final
    }


# Decision Node (pass-through)
def decision_node(state: AgentState):
    return state


# ROUTER 
def route_decision(state: AgentState):
    confidence = state["final_output"].get("confidence", 0.6)

    if confidence < 0.6:
        print("\nLow confidence → Re-running strategy...\n")
        return "strategy"
    else:
        return "end"


# GRAPH BUILD
builder = StateGraph(AgentState)

builder.add_node("strategy", strategy_node)
builder.add_node("analyst", analyst_node)
builder.add_node("decision", decision_node)

builder.set_entry_point("strategy")

builder.add_edge("strategy", "analyst")
builder.add_edge("analyst", "decision")

# Conditional Routing
builder.add_conditional_edges(
    "decision", route_decision,
    {"strategy": "strategy", "end": END}
)

graph = builder.compile()


# RUN
if __name__ == "__main__":
    input_data = {
        "compound": "MEDIUM",
        "tyre_age": 12,
        "circuit": "Bahrain",
        "gap_ahead": 5,
        "gap_behind": 25
    }

    result = graph.invoke({"input_data": input_data})
    
    print("\nFINAL OUTPUT:\n")
    print(result["final_output"])