# 🏎️ F1 AI Race Engineer

An AI-powered Formula 1 race strategy system that combines machine learning, simulation, and multi-agent reasoning to make dynamic race decisions.

---

## 🚀 Project Overview

This project simulates real-time Formula 1 race strategy decisions using:

* Data-driven feature engineering
* Machine learning models
* Tyre degradation simulation
* Multi-agent AI reasoning (LLM-based)

The system evaluates race conditions lap-by-lap and outputs strategic decisions such as:

* PIT NOW
* PIT NOW (UNDERCUT)
* STAY OUT
* DELAY PIT

---

## 🧠 System Architecture

```
Race Simulation Loop
        ↓
Strategy Engine (ML + logic)
        ↓
Strategy Agent (LLM reasoning)
        ↓
Analyst Agent (Critic & validation)
        ↓
Final Decision Output
```

---

## ⚙️ Features

### 🔹 Feature Engineering

* Driver performance metrics
* Pace delta calculation
* Consistency tracking
* Weather classification

### 🔹 Machine Learning Model

* XGBoost regression model
* Predicts position gain
* Evaluated using MAE & Spearman correlation

### 🔹 Tyre Degradation Model

* Predicts lap time loss
* Considers compound, tyre age, and conditions

### 🔹 Strategy Engine

* Simulates pit vs stay decisions
* Undercut modeling
* Gap-based decision logic

### 🔹 Multi-Agent AI System

* **Strategy Agent** → Generates decision with reasoning
* **Analyst Agent** → Critiques and refines decision

### 🔹 Race Simulation

* Lap-by-lap execution
* Stateful decision-making
* Dynamic strategy updates

### 🔹 Fault Tolerance

* Handles LLM JSON failures
* Fallback to deterministic strategy
* Schema-flexible outputs

---

## 📊 Example Output

```
LAP 7
Action: PIT NOW (UNDERCUT)
Confidence: 0.65
Reasoning: Undercut opportunity exists with sufficient gap behind and tyre degradation advantage.
```

---

## 🧩 Tech Stack

* Python
* Pandas / NumPy
* XGBoost
* LangChain
* Ollama (Local LLM)
* Matplotlib (optional)

---

## 📁 Project Structure

```
f1-ai-race-engineer/
│
├── data/
├── ml/
│   ├── feature_engineer.py
│   ├── model_trainer.py
│   ├── tyre_model.py
│   └── strategy_engine.py
│
├── agents/
│   ├── strategy_agent.py
│   └── analyst_agent.py
│
├── simulation/
│   └── race_simulation.py
│
├── models/
├── README.md
└── requirements.txt
```

---

## 🏁 Progress Timeline

### ✅ Day 1–2

* Data pipeline + Feature engineering

### ✅ Day 3

* ML model training + evaluation + SHAP

### ✅ Day 4

* Tyre degradation model + strategy engine

### ✅ Day 5

* Multi-agent system (Strategy + Analyst)
* Race simulation loop
* Fault-tolerant AI pipeline

### 🚀 Day 6 (Next)

* LangGraph orchestration
* Agent workflow graph
* State management system

---

## 🧠 Key Highlights

* Multi-agent AI architecture
* Real-time decision simulation
* Context-aware reasoning
* Hybrid ML + LLM system
* Production-style fault handling

---

## 🎯 Future Improvements

* LangGraph integration
* Streamlit dashboard (UI)
* Safety car & weather modeling
* Full race simulation (multi-driver)

---

## 💡 Inspiration

Inspired by real Formula 1 race strategy systems used by teams to optimize pit stops and race outcomes.

---

## 🏆 Author

Anubhab Pradhan
BE Artificial Intelligence & Data Science
CMR Institute of Technology

---

## ⭐ If you like this project

Give it a star ⭐ on GitHub!
