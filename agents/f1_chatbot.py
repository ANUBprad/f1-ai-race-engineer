import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


# =========================
# LLM
# =========================
llm = ChatOllama(
    model="mistral",   # or llama3
    temperature=0.3
)


# =========================
# PROMPT (VERY IMPORTANT 🔥)
# =========================
prompt = ChatPromptTemplate.from_template("""
You are an elite Formula 1 AI Analyst.

Your role:
- Answer F1-related questions accurately
- Explain strategies (undercut, tyre wear, pit stops)
- Provide structured and insightful answers
- Think like a race engineer, not a fan

Guidelines:
- Keep answers clear and professional
- Use racing terminology when needed
- If applicable, break answer into sections
- Avoid generic responses

User Question:
{question}

Provide a high-quality answer.
""")


# =========================
# CHAIN
# =========================
chain = prompt | llm


# =========================
# CHAT FUNCTION
# =========================
def ask_f1(question: str):
    response = chain.invoke({
        "question": question
    })
    return response.content


# =========================
# CLI LOOP (TEST MODE)
# =========================
if __name__ == "__main__":

    print("\n🏎️ F1 AI Analyst Chatbot (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        answer = ask_f1(user_input)

        print("\n🤖 Analyst:\n")
        print(answer)
        print("\n" + "-"*50 + "\n")