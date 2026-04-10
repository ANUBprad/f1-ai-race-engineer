🏎️ F1 AI Race Engineer

An intelligent, end-to-end Formula 1 race strategy system that combines machine learning, simulation, and multi-agent AI to make real-time race decisions.

---

🚀 Project Overview

This system simulates how real F1 teams make strategic decisions during a race. It integrates:

- Data ingestion from real F1 sessions
- Machine learning for predictive modeling
- Simulation-based decision logic
- Multi-agent AI reasoning with self-correction

The system operates in a loop, evaluating race conditions lap-by-lap and producing strategic decisions with explanations and confidence scores.

---

🧠 System Architecture

Telemetry/Data → Feature Engineering → ML Models
                         ↓
                Strategy Engine (Simulation)
                         ↓
          Strategy Agent (LLM Reasoning)
                         ↓
           Analyst Agent (Critique Layer)
                         ↓
                Final Decision Output

---

⚙️ Core Capabilities

- 📊 Predict race outcomes using ML
- 🛞 Model tyre degradation dynamically
- 🧠 Generate strategic decisions using AI agents
- 🔁 Simulate races lap-by-lap
- 🛡️ Handle uncertainty with fallback mechanisms
- 📉 Provide explainable reasoning + confidence

---

🏗️ Project Phases

---

🔹 Phase 1: Data Pipeline & Feature Engineering

- Built pipeline using FastF1
- Extracted race, lap, and weather data
- Engineered features like:
  - Pace delta
  - Driver consistency
  - Grid advantage
- Created structured dataset for ML training

---

🔹 Phase 2: Machine Learning Models

- Trained XGBoost regression model
- Target: Position gain
- Evaluated using:
  - Mean Absolute Error (MAE)
  - Spearman Rank Correlation
- Added SHAP for explainability

---

🔹 Phase 3: Tyre Degradation Modeling

- Built regression model for lap time loss
- Inputs:
  - Tyre compound
  - Tyre age
  - Track conditions
- Output:
  - Predicted degradation curve

---

🔹 Phase 4: Strategy Engine (Simulation Core)

- Simulates:
  - Stay-out vs pit scenarios
  - Undercut opportunities
  - Gap-based decisions
- Produces:
  - Action + confidence score

---

🔹 Phase 5: Multi-Agent AI System

- Strategy Agent
  - Enhances decisions using LLM reasoning
- Analyst Agent
  - Critiques and refines decisions
- Features:
  - JSON-structured outputs
  - Confidence calibration
  - Fault-tolerant fallback system

---

🔹 Next Phase: LangGraph Orchestration 🚀

- Convert pipeline into graph-based execution
- Introduce:
  - Stateful agents
  - Conditional flows
  - Multi-step reasoning loops

---

🔁 Race Simulation

- Lap-by-lap simulation engine
- Dynamic updates:
  - Tyre age
  - Gaps
  - Strategy decisions
- Produces evolving race strategy

---

📊 Example Output

LAP 7
Action: PIT NOW (UNDERCUT)
Confidence: 0.65
Reasoning: Undercut opportunity exists with sufficient gap behind and tyre degradation advantage.

---

🧩 Tech Stack

- Python
- Pandas / NumPy
- XGBoost
- SHAP
- LangChain
- Ollama (Local LLM)

---

📁 Project Structure

f1-ai-race-engineer/
│
├── data/
├── ml/
├── agents/
├── simulation/
├── models/
├── README.md
└── requirements.txt

---

🧠 Key Highlights

- Multi-agent AI architecture
- Hybrid ML + LLM system
- Simulation-driven decision making
- Explainable AI with SHAP
- Production-style fault tolerance

---

🎯 Future Enhancements

- LangGraph-based orchestration
- Streamlit dashboard
- Safety car & weather simulation
- Full multi-driver race simulation

---

👨‍💻 Author

Anubhab Pradhan
BE Artificial Intelligence & Data Science
CMR Institute of Technology

---

⭐ Support

If you find this project interesting, consider giving it a star ⭐