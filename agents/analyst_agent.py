import sys
import os
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# LLM
llm = ChatOllama(model="mistral", temperature=0)

# Prompt
prompt = ChatPromptTemplate.from_template("""
You are a senior Formula 1 race strategist reviewing a decision.

Initial Decision: {decision}

Context:
- Compound: {compound}
- Tyre Age: {tyre_age}
- Circuit: {circuit}
- Gap Ahead: {gap_ahead}
- Gap Behind: {gap_behind}

Tasks:
1. Critically analyze the decision
2. Identify risks or weaknesses
3. Either confirm or adjust decision
4. Adjust confidence realistically

Use ONLY these actions:
- PIT NOW
- PIT NOW (UNDERCUT)
- STAY OUT
- DELAY PIT
                                          
Return STRICT VALID JSON.
- No trailing commas
- No extra text
- Do not include confidence inside reasoning
""")
parser = JsonOutputParser()
chain = prompt | llm | parser

# Function
def analyze_decision(input_data, initial_decision):
    return chain.invoke({
        **input_data, "decision": initial_decision
    })
    