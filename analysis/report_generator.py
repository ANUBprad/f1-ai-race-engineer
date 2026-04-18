import sys
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) # Add root path for imports

from langchain_ollama import ChatOllama
from analysis.sample_data import generate_race_data

# LLM SETUP
llm = ChatOllama(model="mistral", temperature=0.3)

# INSIGHT GENERATION
def generate_insights(data):

    avg_lap = sum(data["lap_times"]) / len(data["lap_times"])
    max_deg = max(data["degradation"])

    # Detect trend
    if data["lap_times"][-1] > data["lap_times"][0]:
        trend = "increasing lap times due to tyre degradation"
    else:
        trend = "stable performance"

    return {
        "avg_lap_time": round(avg_lap, 2),
        "max_degradation": max_deg,
        "trend": trend
    }


# REPORT GENERATION (LLM)
def generate_report(insights):

    prompt = f"""
        You are a Formula 1 race analyst.

        Generate a professional race report using:

        Average Lap Time: {insights['avg_lap_time']}
        Max Tyre Degradation: {insights['max_degradation']}
        Performance Trend: {insights['trend']}

        Structure your response clearly:

        - Race Summary
        - Key Insight
        - Performance Analysis

        Keep it concise (5-6 lines).
        Use F1-style terminology.
        """

    response = llm.invoke(prompt)
    return response.content


# MAIN EXECUTION
if __name__ == "__main__":

    print("\nGenerating Race Report...\n")

    data = generate_race_data()
    insights = generate_insights(data)

    print("📊 Insights:")
    for k, v in insights.items():
        print(f"- {k}: {v}")

    report = generate_report(insights)
    print("\n" + "="*50)
    print("F1 RACE REPORT")
    print("="*50)
    print(report)