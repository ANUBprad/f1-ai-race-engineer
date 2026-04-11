# 🏎️ F1 AI Race Engineer

> An end-to-end AI-powered Formula 1 race strategy system — combining real telemetry, machine learning, tyre degradation modeling, and multi-agent reasoning to make lap-by-lap strategic decisions.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![XGBoost](https://img.shields.io/badge/XGBoost-ML-orange?style=flat-square)
![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-purple?style=flat-square)
![FastF1](https://img.shields.io/badge/FastF1-Telemetry-red?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📌 What Is This?

Real F1 teams have race engineers who analyze telemetry, tyre wear, gaps, and weather to decide *exactly when* to pit. This project replicates that system using AI.

The pipeline processes live-style race inputs lap-by-lap and outputs a **decision** (PIT NOW / STAY OUT / DELAY PIT), a **confidence score**, and **human-readable reasoning** — just like a real race engineer would radio to the driver.

---

## 🧠 System Architecture

```
FastF1 Telemetry / Race Input
         │
         ▼
 Feature Engineering
 (pace delta, consistency, grid advantage)
         │
         ▼
  ML Models (XGBoost)
  + Tyre Degradation Model
         │
         ▼
  Strategy Engine
  (pit vs stay vs undercut simulation)
         │
         ▼
  Strategy Agent  ──►  Analyst Agent
  (LLM reasoning)      (critique & refine)
         │
         ▼
  LangGraph Orchestration
  (stateful, conditional, self-correcting)
         │
         ▼
   Final Decision Output
   { action | confidence | reasoning }
```

---

## ⚙️ Core Capabilities

| Capability | Description |
|---|---|
| 🛞 Tyre Degradation Modeling | Predicts lap time loss based on compound, age, and track conditions |
| 📈 ML Race Prediction | XGBoost model predicts position gain from engineered features |
| ⚙️ Strategy Simulation | Evaluates pit, stay-out, and undercut scenarios with gap logic |
| 🧠 Multi-Agent Reasoning | Strategy Agent generates decisions; Analyst Agent critiques them |
| 🔁 Lap-by-Lap Simulation | Full race loop with dynamic tyre age and gap updates |
| 🔀 LangGraph Orchestration | Graph-based execution with stateful nodes and feedback loops |
| 🛡️ Fault-Tolerant Pipeline | Graceful fallback when LLM calls fail or confidence is low |
| 📊 Explainable AI | SHAP values + reasoning traces for every decision |

---

## 🏗️ Build Phases

<details>
<summary><strong>Phase 1 — Data Pipeline & Feature Engineering</strong></summary>

- Ingested real race data using **FastF1**
- Extracted lap times, tyre data, weather, and grid positions
- Engineered features: pace delta, driver consistency, grid advantage
- Built structured dataset for model training

</details>

<details>
<summary><strong>Phase 2 — Machine Learning Modeling</strong></summary>

- Trained **XGBoost regression model** to predict position gain
- Evaluated with MAE and Spearman Rank Correlation
- Integrated **SHAP** for feature explainability

</details>

<details>
<summary><strong>Phase 3 — Tyre Degradation Model</strong></summary>

- Modeled lap time degradation as a function of compound, age, and conditions
- Output: a degradation curve used downstream in strategy simulation

</details>

<details>
<summary><strong>Phase 4 — Strategy Engine</strong></summary>

- Simulates stay-out, pit, and undercut scenarios
- Uses gap-to-car-ahead/behind logic
- Outputs an action + confidence score per lap

</details>

<details>
<summary><strong>Phase 5 — Multi-Agent AI System</strong></summary>

- **Strategy Agent**: generates a decision using LLM reasoning over race state
- **Analyst Agent**: critiques the decision and refines it
- Structured JSON outputs with confidence calibration
- Fault-tolerant fallback to simulation when LLM fails

</details>

<details>
<summary><strong>Phase 6 — LangGraph Orchestration ✅</strong></summary>

- Entire pipeline converted to a **stateful graph**
- Node-based workflow with conditional routing
- Self-correcting feedback loop between agents
- Supports multi-step reasoning across laps

</details>

---

## 📊 Example Output

```
═══════════════════════════════
  LAP 7 — STRATEGY DECISION
═══════════════════════════════
  Action     : PIT NOW (UNDERCUT)
  Confidence : 0.65
  Reasoning  : Undercut window is open. Gap behind is 25s —
               sufficient to cover a pit stop. Tyre degradation
               on the current MEDIUM set is accelerating.
               Competitor ahead has not pitted; pit now to
               jump them on fresh rubber.
═══════════════════════════════
```

---

## 📁 Project Structure

```
f1-ai-race-engineer/
│
├── agents/
│   ├── strategy_agent.py       # LLM-based decision generation
│   ├── analyst_agent.py        # Critique and refinement layer
│   └── langgraph_flow.py       # Graph orchestration
│
├── ml/
│   ├── feature_engineer.py     # Feature extraction from FastF1
│   ├── model_trainer.py        # XGBoost training pipeline
│   ├── tyre_model.py           # Degradation curve modeling
│   └── strategy_engine.py      # Simulation core (pit vs stay)
│
├── simulation/
│   └── race_simulation.py      # Lap-by-lap race loop
│
├── dashboard/                  # (WIP) Streamlit UI
├── src/                        # Shared utilities
├── data/                       # Race data (FastF1 cache)
├── models/                     # Saved ML model artifacts
│
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai) installed and running locally (for the LLM agents)

### Installation

```bash
git clone https://github.com/ANUBprad/f1-ai-race-engineer.git
cd f1-ai-race-engineer
pip install -r requirements.txt
```

### Run the Race Simulation

```bash
python simulation/race_simulation.py
```

### Run the Full Multi-Agent System (LangGraph)

```bash
python agents/langgraph_flow.py
```

---

## 🧪 Try Your Own Scenario

Open `simulation/race_simulation.py` and modify the input state:

```python
input_data = {
    "compound": "MEDIUM",   # SOFT / MEDIUM / HARD
    "tyre_age": 12,          # laps on current set
    "circuit": "Bahrain",
    "gap_ahead": 5.2,        # seconds to car ahead
    "gap_behind": 25.0       # seconds to car behind
}
```

Then re-run to see how the strategy adapts.

---

## 🧩 Tech Stack

| Layer | Tools |
|---|---|
| Data | FastF1, Pandas, NumPy |
| ML | XGBoost, SHAP |
| Simulation | Custom Python engine |
| Agents | LangChain, Ollama (local LLM) |
| Orchestration | LangGraph |
| Dashboard (WIP) | Streamlit |

---

## 🎯 Roadmap

- [x] Data pipeline with FastF1
- [x] XGBoost race performance model
- [x] Tyre degradation model
- [x] Strategy simulation engine
- [x] Multi-agent system (Strategy + Analyst)
- [x] LangGraph orchestration with feedback loop
- [ ] Streamlit interactive dashboard
- [ ] Safety car & weather event modeling
- [ ] Multi-driver full race simulation
- [ ] Live telemetry integration

---

## 👨‍💻 Author

**Anubhab Pradhan**  
