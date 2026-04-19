import sys
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) # Add root path for imports

from langchain_ollama import ChatOllama
from analysis.sample_data import generate_race_data
from ml.strategy_engine import StrategyEngine
from analysis.visualization import generate_all_plots

# LLM SETUP
llm = ChatOllama(model="mistral", temperature=0.3)

# INSIGHT GENERATION
def generate_insights(data):
    lap_times = data["lap_times"]
    avg_lap = sum(lap_times) / len(lap_times)
    max_deg = max(data["degradation"])

    # Trend
    trend = "increasing" if lap_times[-1] > lap_times[0] else "stable"

    # Critical lap detection
    deltas = [lap_times[i] - lap_times[i-1] for i in range(1, len(lap_times))]
    critical_lap = deltas.index(max(deltas)) + 2  # +2 because index shift

    return {
        "avg_lap_time": round(avg_lap, 2),
        "max_degradation": max_deg,
        "trend": trend,
        "critical_lap": critical_lap
    }


def generate_strategy_insight(data):
    engine = StrategyEngine()
    tyre_age = len(data["lap_times"]) // 2
    result = engine.decide(
        compound="MEDIUM",
        tyre_age=tyre_age,
        circuit="Bahrain",
        gap_ahead=5,
        gap_behind=20
    )
    return result


# REPORT GENERATION (LLM)
def generate_report(insights, strategy):

    prompt = f"""
        You are a professional Formula 1 race analyst.

        Race Data:
        - Average Lap Time: {insights['avg_lap_time']}
        - Max Degradation: {insights['max_degradation']}
        - Trend: {insights['trend']}
        - Critical Lap: {insights['critical_lap']}

        Strategy Decision:
        - Action: {strategy['action']}
        - Confidence: {strategy['confidence']}

        Generate a structured report:
        1. Race Summary
        2. Key Performance Insight
        3. Critical Moment Analysis
        4. Strategy Evaluation
        5. Final Recommendation

        Keep it concise but insightful.
        Use real F1 terminology.
        """

    response = llm.invoke(prompt)
    return response.content


# MAIN EXECUTION
if __name__ == "__main__":

    print("\n" + "="*50)
    print("F1 RACE REPORT")
    print("="*50)

    data = generate_race_data()
    insights = generate_insights(data)
    strategy = generate_strategy_insight(data)
    generate_all_plots(data)

    print("\nInsights:")
    for k, v in insights.items():
        print(f"- {k}: {v}")

    print("\nStrategy Decision:")
    print(f"- Action: {strategy['action']}")
    print(f"- Confidence: {round(strategy['confidence']*100)}%")
    print(f"- Reasoning: {strategy['reasoning'].replace('.', '. ')}")

    report = generate_report(insights, strategy)

    print("\nRace Report:\n")
    print(report)