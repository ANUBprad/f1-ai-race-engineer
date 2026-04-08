import sys
import os

from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from ml.strategy_engine import StrategyEngine


# =========================
# Initialize Engine
# =========================
engine = StrategyEngine()


# =========================
# Strategy Tool
# =========================
def strategy_tool(input_data):
    return engine.decide(
        compound=input_data["compound"],
        tyre_age=input_data["tyre_age"],
        circuit=input_data["circuit"],
        gap_ahead=input_data["gap_ahead"],
        gap_behind=input_data["gap_behind"]
    )


# =========================
# LLM (Ollama - Stable)
# =========================
llm = ChatOllama(
    model="mistral",   # or "llama3"
    temperature=0
)


# =========================
# Prompt (STRICT JSON)
# =========================
prompt = ChatPromptTemplate.from_template("""
You are an elite Formula 1 race engineer.

Race State:
- Compound: {compound}
- Tyre Age: {tyre_age}
- Circuit: {circuit}
- Gap Ahead: {gap_ahead}s
- Gap Behind: {gap_behind}s

Strategy engine output:
{strategy_output}

Instructions:
- DO NOT change the decision unless clearly wrong
- Improve explanation quality
- Adjust confidence realistically (0.5–0.9 range)

Return ONLY JSON:
{{
  "action": "...",
  "reasoning": "...",
  "confidence": float
}}
""")


# =========================
# Chain
# =========================
parser = JsonOutputParser()
chain = prompt | llm | parser


# =========================
# Run
# =========================
if __name__ == "__main__":
    input_data = {
        "compound": "MEDIUM",
        "tyre_age": 12,
        "circuit": "Bahrain",
        "gap_ahead": 5,
        "gap_behind": 25
    }

    strategy_output = strategy_tool(input_data)

    print("\nRaw Strategy Engine Output:")
    print(strategy_output)

    response = chain.invoke({**input_data,
        "strategy_output": strategy_output
    })

    print("\nAI Strategy Decision:\n")
    print(response)