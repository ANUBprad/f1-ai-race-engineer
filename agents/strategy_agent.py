import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from ml.strategy_engine import StrategyEngine
from agents.analyst_agent import analyze_decision


# Initialize Engine
engine = StrategyEngine()


# Strategy Tool
def strategy_tool(input_data):
    return engine.decide(
        compound=input_data["compound"],
        tyre_age=input_data["tyre_age"],
        circuit=input_data["circuit"],
        gap_ahead=input_data["gap_ahead"],
        gap_behind=input_data["gap_behind"]
    )


# LLM (Ollama)
llm = ChatOllama(model="mistral", temperature=0)


# Prompt
prompt = ChatPromptTemplate.from_template("""
You are an elite Formula 1 race engineer.

Race State:
- Compound: {compound}
- Tyre Age: {tyre_age}
- Circuit: {circuit}
- Gap Ahead: {gap_ahead}s
- Gap Behind: {gap_behind}s

Strategy engine output: {strategy_output}

Instructions:
- DO NOT change decision unless clearly wrong
- Improve explanation quality
- Adjust confidence realistically (0.5–0.9 range)

Use ONLY these actions:
- PIT NOW
- PIT NOW (UNDERCUT)
- STAY OUT
- DELAY PIT                                

Return STRICT VALID JSON.
- No trailing commas
- No extra text
- Do not include confidence inside reasoning
{{
  "action": "...",
  "reasoning": "...",
  "confidence": float
}}
""")


# Chain
parser = JsonOutputParser()
chain = prompt | llm | parser


# MAIN FUNCTION 
def run_strategy(input_data, history=None):

    # Step 1: Strategy Engine
    strategy_output = strategy_tool(input_data)

    # Step 2: Strategy Agent (LLM)
    try:
        ai_decision = chain.invoke({
            **input_data,
            "strategy_output": strategy_output
        })
    except Exception:
        print("⚠️ Strategy Agent failed, using fallback...")

        ai_decision = chain.invoke({
            **input_data,
            "strategy_output": strategy_output,
            "history": history or []
        })

    # Step 3: Analyst Agent (Critic)
    try:
        final_decision = analyze_decision(input_data, ai_decision)
    except Exception:
        print("⚠️ Analyst Agent failed, using AI decision...")

        final_decision = {
            "final_action": ai_decision.get("action"),
            "analysis": ai_decision.get("reasoning"),
            "confidence": ai_decision.get("confidence", 0.6)
        }

    # Step 4: Final Output
    final_output = {
        "action": final_decision.get("final_action") or final_decision.get("action"),
        "confidence": float(final_decision.get("confidence", 0.6)),
        "reasoning": final_decision.get("analysis") or final_decision.get("reasoning")
    }

    return final_output

#==================================
if __name__ == "__main__":

    input_data = {
        "compound": "MEDIUM",
        "tyre_age": 12,
        "circuit": "Bahrain",
        "gap_ahead": 5,
        "gap_behind": 25
    }

    result = run_strategy(input_data)

    print("\n🏁 FINAL DECISION:\n")
    print(result)