import sys
import os
import re
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from agents.strategy_agent import run_strategy


# =========================
# LLM
# =========================
llm = ChatOllama(
    model="mistral",
    temperature=0.3
)


# =========================
# MEMORY
# =========================
chat_history = []


# =========================
# PROMPT (MULTI-MODE)
# =========================
prompt = ChatPromptTemplate.from_template("""
You are an elite Formula 1 AI Analyst 🏎️.

Mode: {mode}

Chat History:
{history}

User Question:
{question}

Behavior Rules:

If Mode = KNOWLEDGE:
- Provide structured explanation
- Be detailed and insightful
- Use:
  Explanation
  Key Insight
  Example

If Mode = STRATEGY:
- Be concise and action-focused
- Think like a race engineer
- Focus on decision-making

If Mode = HYBRID:
- First explain the concept clearly
- Then connect it to a real race scenario
- Keep it engaging and insightful

General:
- Keep responses energetic and engaging
- If question is not directly F1-related:
  → briefly acknowledge it
  → relate it back to F1
- Maintain racing tone

Answer:
""")

chain = prompt | llm


# =========================
# INTENT DETECTION (LLM)
# =========================
def detect_intent(question):

    intent_prompt = f"""
Classify the user query into ONE of these categories:

1. STRATEGY → asking what decision to take (pit, tyres, gaps, etc.)
2. KNOWLEDGE → asking for explanation or info about F1
3. HYBRID → asking for explanation + decision/example

Return ONLY one word: STRATEGY or KNOWLEDGE or HYBRID

Query:
{question}
"""

    response = llm.invoke(intent_prompt)

    intent = response.content.strip().upper()

    if "STRATEGY" in intent:
        return "STRATEGY"
    elif "HYBRID" in intent:
        return "HYBRID"
    else:
        return "KNOWLEDGE"


# =========================
# EXTRACT NUMBERS
# =========================
def extract_values(question):
    numbers = list(map(int, re.findall(r'\d+', question)))

    return {
        "tyre_age": numbers[0] if len(numbers) > 0 else 10,
        "gap_ahead": numbers[1] if len(numbers) > 1 else 5,
        "gap_behind": numbers[2] if len(numbers) > 2 else 20
    }


# =========================
# MAIN CHAT FUNCTION
# =========================
def ask_f1(question):

    global chat_history

    intent = detect_intent(question)
    history_text = "\n".join(chat_history[-4:])

    # =========================
    # STRATEGY MODE
    # =========================
    if intent == "STRATEGY":

        values = extract_values(question)

        input_data = {
            "compound": "MEDIUM",
            "tyre_age": values["tyre_age"],
            "circuit": "Bahrain",
            "gap_ahead": values["gap_ahead"],
            "gap_behind": values["gap_behind"]
        }

        result = run_strategy(input_data)

        return f"""
            🏁 Strategy Recommendation:
            Action: {result['action']}
            Confidence: {result['confidence']}
            Reasoning:
            {result['reasoning']}
            """

    # HYBRID MODE
    elif intent == "HYBRID":
        explanation = chain.invoke({
            "question": question,
            "history": history_text,
            "mode": "HYBRID"
        }).content
        values = extract_values(question)

        input_data = {
            "compound": "MEDIUM",
            "tyre_age": values["tyre_age"],
            "circuit": "Bahrain",
            "gap_ahead": values["gap_ahead"],
            "gap_behind": values["gap_behind"]
        }
        result = run_strategy(input_data)

        return f"""
            {explanation}
            🏁 Example Strategy Scenario:
            Action: {result['action']}
            Confidence: {result['confidence']}
            """

    # KNOWLEDGE MODE
    else:
        response = chain.invoke({
            "question": question,
            "history": history_text,
            "mode": "KNOWLEDGE"
        })
        answer = response.content

        chat_history.append(f"User: {question}")
        chat_history.append(f"Bot: {answer}")

        return answer


# CLI LOOP
if __name__ == "__main__":
    print("\n🏎️ F1 AI Analyst (Multi-Mode) — type 'exit' to quit\n")
    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        answer = ask_f1(user_input)

        print("\n🤖 Analyst:\n")
        print(answer)
        print("\n" + "-" * 50 + "\n")