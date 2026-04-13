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
# PROMPT
# =========================
prompt = ChatPromptTemplate.from_template("""
You are an elite Formula 1 AI Analyst 🏎️.

Behavior:
- Always keep responses engaging, energetic, and insightful
- If the question is NOT about F1:
  → briefly acknowledge it
  → creatively relate it back to Formula 1
  → maintain a racing tone
- Never reject the user

Chat History:
{history}

User Question:
{question}

Instructions:
- Think like a race engineer
- Use clear structure
- Be concise but insightful

Structure:
- Explanation
- Key Insight
- Example (if applicable)

Answer:
""")

chain = prompt | llm


# =========================
# DETECT STRATEGY QUERY
# =========================
def is_strategy_query(question):
    keywords = ["tyre", "pit", "gap", "strategy", "lap", "undercut", "overcut"]
    return any(word in question.lower() for word in keywords)


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

    # 🔥 STRATEGY MODE (CALL YOUR SYSTEM)
    if is_strategy_query(question):

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

    # 🔥 NORMAL / REDIRECT FLOW
    history_text = "\n".join(chat_history[-4:])

    response = chain.invoke({
        "question": question,
        "history": history_text
    })

    answer = response.content

    # Store memory
    chat_history.append(f"User: {question}")
    chat_history.append(f"Bot: {answer}")

    return answer


# =========================
# CLI LOOP
# =========================
if __name__ == "__main__":

    print("\n🏎️ F1 AI Analyst (Enhanced Mode) — type 'exit' to quit\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        answer = ask_f1(user_input)

        print("\n🤖 Analyst:\n")
        print(answer)
        print("\n" + "-" * 50 + "\n")