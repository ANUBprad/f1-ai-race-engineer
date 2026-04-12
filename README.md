# F1 AI Race Engineer 🏎️

Ever watched an F1 race and wondered what's actually going on in that garage when an engineer says "box, box, box"? This project tries to answer that — by building an AI that thinks like a race strategist.

It's not just a chatbot. It's a full decision-making pipeline that combines machine learning, tyre physics simulation, and multi-agent AI to figure out *when* to pit, *why*, and *how confident* we should be about that call.

---

## What it does

Feed it a race state — lap number, tyre compound, gap to the car ahead — and it'll tell you:

- **PIT NOW / STAY OUT / DELAY PIT**
- A confidence score
- The reasoning behind the call, in plain English

```
LAP 7
Action: PIT NOW (UNDERCUT)
Confidence: 0.65
Reasoning: Undercut opportunity exists with sufficient gap behind and tyre degradation advantage.
```

---

## How it's built

The system works in layers, each feeding into the next:

```
Race state input
    ↓
Feature engineering + ML model (XGBoost)
    ↓
Tyre degradation model
    ↓
Strategy engine — simulates pit vs. stay-out scenarios
    ↓
Strategy Agent — makes the call, writes the reasoning
    ↓
Analyst Agent — critiques it, refines if needed
    ↓
LangGraph — orchestrates the whole flow with feedback loops
    ↓
Decision output
```

The ML model estimates position gain. The simulation engine plays out different scenarios. The agents argue about it. LangGraph keeps the state clean and lets the system self-correct.

---

## Project phases

### Phase 1 — Data pipeline
Took raw race data and turned it into something useful. Built features like `pace_delta`, `driver_consistency`, and `grid_advantage`. Nothing glamorous, but everything downstream depends on getting this right.

### Phase 2 — ML model
Trained an XGBoost regression model to predict `position_gain`. Evaluated with MAE and Spearman rank correlation. Added SHAP so you can actually see *which features* are driving the prediction — not just trust the black box.

### Phase 3 — Tyre degradation model
Built a model that simulates how a tyre degrades lap-by-lap based on compound, age, and conditions. This is what gives the strategy engine its teeth — without realistic degradation curves, pit stop timing is just a guess.

### Phase 4 — Strategy engine
The simulation core. It runs the numbers on staying out vs. pitting, models the time lost in the pit lane, accumulates degradation, and flags undercut windows. Output is an action and a confidence score.

### Phase 5 — Multi-agent AI
Two agents on top of the simulation layer:
- **Strategy Agent** — takes the simulation output, makes a decision, explains the reasoning
- **Analyst Agent** — reads that reasoning, looks for holes, refines the output

The result feels surprisingly human. It doesn't just output "PIT NOW" — it tells you *why*, in the way an engineer might actually phrase it.

### Phase 6 — LangGraph orchestration
Converted the whole pipeline into a proper graph-based system. Nodes, conditional routing, stateful execution, and a feedback loop so the system can catch and correct bad outputs. This is what makes it feel production-grade rather than a Jupyter notebook.

### Phase 7 — F1 Knowledge Chatbot *(in progress)*
There's an early-stage chatbot built with Ollama + LangChain that answers F1 strategy questions. Right now it's fairly simple Q&A, but the plan is to wire it into the strategy engine so it can give context-aware answers based on actual race state — not just general knowledge.

Planned additions:
- Conversation memory
- Hybrid chatbot + decision system
- RAG for factual accuracy on historical data

---

## Try it yourself

```bash
git clone <your-repo-link>
cd f1-ai-race-engineer
pip install -r requirements.txt
```

Run the race simulation:
```bash
python simulation/race_simulation.py
```

Run the full LangGraph system:
```bash
python agents/langgraph_flow.py
```

Run the chatbot:
```bash
python agents/f1_chatbot.py
```

To test your own scenario, just edit the input in the simulation script:

```python
input_data = {
    "compound": "MEDIUM",
    "tyre_age": 12,
    "circuit": "Bahrain",
    "gap_ahead": 5,
    "gap_behind": 25
}
```

---

## Project structure

```
f1-ai-race-engineer/
├── data/
├── ml/
│   ├── model_trainer.py
│   ├── tyre_model.py
│   └── strategy_engine.py
├── agents/
│   ├── strategy_agent.py
│   ├── analyst_agent.py
│   ├── langgraph_flow.py
│   └── f1_chatbot.py
├── simulation/
│   └── race_simulation.py
├── models/
└── README.md
```

---

## Stack

Python · Pandas · NumPy · XGBoost · SHAP · LangChain · LangGraph · Ollama

---

## What's next

- Race Report Generator — visual summaries with lap-by-lap insights
- Race Result Predictor — probability-based outcome forecasting
- Streamlit dashboard — interactive UI to explore strategies in real time

---

## About

Built by **Anubhab Pradhan**

This started as a curiosity about how F1 teams actually make real-time decisions under pressure. It turned into a proper ML + AI system. Still a lot left to build — but the core is working.

If you find it useful or interesting, a ⭐ goes a long way.
