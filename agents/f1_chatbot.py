import sys
import os
import re
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from agents.strategy_agent import run_strategy

# LLM
llm = ChatOllama(model="mistral", temperature=0.3)

# MEMORY STATE
memory = {"history": [], "topic": None}

# PROMPT (MULTI-MODE + CONTEXT)
prompt = ChatPromptTemplate.from_template("""
You are an elite Formula 1 AI Analyst.

Mode: {mode}
Current Topic: {topic}
Conversation Context: {history}
User Question: {question}

Instructions:
- Maintain continuity with previous conversation
- Avoid repeating explanations unnecessarily
- Build on previous responses

Behavior Rules:

If Mode = KNOWLEDGE:
- Provide structured explanation
- Use:
  Explanation
  Key Insight
  Example

If Mode = STRATEGY:
- Be concise and decision-focused

If Mode = HYBRID:
- Explain + connect to real scenario

General:
- Keep responses engaging and energetic
- If not directly F1-related → relate it back to F1

Answer:
""")
chain = prompt | llm


# INTENT DETECTION
def detect_intent(question):

    intent_prompt = f"""
        Classify the user query into ONE of these categories:
        1. STRATEGY
        2. KNOWLEDGE
        3. HYBRID

        Return ONLY one word.
        Query: {question}
    """

    response = llm.invoke(intent_prompt)
    intent = response.content.strip().upper()

    if "STRATEGY" in intent:
        return "STRATEGY"
    elif "HYBRID" in intent:
        return "HYBRID"
    else:
        return "KNOWLEDGE"


# TOPIC DETECTION
def detect_topic(question):

    q = question.lower()

    if "undercut" in q or "overcut" in q:
        return "strategy_concept"
    elif "tyre" in q or "degradation" in q:
        return "tyre"
    elif "driver" in q or "team" in q:
        return "f1_entities"
    else:
        return "general"


# MEMORY FUNCTIONS
def update_memory(question, answer):
    topic = detect_topic(question)
    memory["topic"] = topic
    memory["history"].append({"user": question, "bot": answer})
    memory["history"] = memory["history"][-5:]


def build_context():
    history_text = ""

    for chat in memory["history"]:
        history_text += f"User: {chat['user']}\n"
        history_text += f"Bot: {chat['bot']}\n"

    return history_text


# EXTRACT VALUES
def extract_values(question):
    numbers = list(map(int, re.findall(r'\d+', question)))

    return {
        "tyre_age": numbers[0] if len(numbers) > 0 else 10,
        "gap_ahead": numbers[1] if len(numbers) > 1 else 5,
        "gap_behind": numbers[2] if len(numbers) > 2 else 20
    }


# SCENARIO BUILDER 
def build_scenario(question):

    q = question.lower()
    scenario = {
        "compound": "MEDIUM",
        "tyre_age": 10,
        "gap_ahead": 5,
        "gap_behind": 20,
        "circuit": "Bahrain"
    }

    if "undercut" in q:
        scenario["tyre_age"] = 12
        scenario["gap_ahead"] = 4
    elif "overcut" in q:
        scenario["tyre_age"] = 6
        scenario["gap_ahead"] = 2
    elif "degradation" in q:
        scenario["tyre_age"] = 15

    return scenario


# STRATEGY EXPLAINER
def explain_strategy(result):

    explanation_prompt = f"""
        You are a Formula 1 race engineer.

        Explain why this strategy works:

        Decision: {result['action']}
        Confidence: {result['confidence']}
        Reasoning: {result['reasoning']}
        """

    response = llm.invoke(explanation_prompt)
    return response.content


# MAIN FUNCTION
def ask_f1(question):

    intent = detect_intent(question)
    history_text = build_context()
    topic = detect_topic(question)

    # STRATEGY MODE
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

        answer = f"""
            Strategy Recommendation:

            Action: {result['action']}
            Confidence: {result['confidence']}

            Reasoning: {result['reasoning']}
            """

        update_memory(question, answer)
        return answer

    # HYBRID MODE
    elif intent == "HYBRID":
        explanation = chain.invoke({
            "question": question,
            "history": history_text,
            "mode": "HYBRID",
            "topic": topic
        }).content

        scenario = build_scenario(question)
        result = run_strategy(scenario)
        strategy_explanation = explain_strategy(result)

        answer = f"""
            {explanation}

            🏁 Real Race Scenario Simulation:

            Action: {result['action']}
            Confidence: {result['confidence']}
            🔧 Why this works: {strategy_explanation}
            """

        update_memory(question, answer)
        return answer

    # KNOWLEDGE MODE
    else:
        response = chain.invoke({
            "question": question,
            "history": history_text,
            "mode": "KNOWLEDGE",
            "topic": topic
        })

        answer = response.content
        update_memory(question, answer)
        return answer


# CLI LOOP
if __name__ == "__main__":

    print("\n F1 AI Analyst (Advanced Mode) — type 'exit' to quit\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        answer = ask_f1(user_input)

        print("\n Analyst:\n")
        print(answer)
        print("\n" + "-" * 50 + "\n")