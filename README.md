# F1 AI Race Engineer 🏁

I've always been fascinated by the moment a race engineer says "box, box" — and the entire race pivots on that call. This project is my attempt to understand (and rebuild) that decision-making process from the ground up.

It started as a curiosity. It became a full pipeline that analyzes real telemetry, models tyre degradation, and reasons through strategy — the way an actual pit wall would.

---

## What does it actually do?

Given a live race state — lap number, tyre compound, gaps to cars ahead and behind — the system produces:

- **A strategy call** → PIT / STAY OUT / DELAY PIT
- **A confidence score** → how sure it is
- **Engineer-style reasoning** → not generic AI output, but something that sounds like it came from someone who's watched 500 hours of F1

Here's what a typical output looks like:

```
LAP 12
Decision: PIT NOW
Confidence: 0.68
Reason: Undercut possible with sufficient gap and rising degradation.
```

---

## How it's built

The core idea was to avoid just throwing an LLM at the problem. Real strategy is physics + data + intuition. So the architecture reflects that:

```
Race Inputs
   ↓
Feature Engineering + ML Model
   ↓
Tyre Degradation Model
   ↓
Strategy Engine (simulation)
   ↓
AI Reasoning Layer
   ↓
Final Decision
```

Each layer does something meaningful before passing it on.

---

## How it came together — Phase by Phase

### Phase 1 — Data Pipeline
Started with raw race data and had to make it usable. Built features like `pace_delta` and consistency scores. A lot of unglamorous cleaning work, but it set the foundation for everything else.

### Phase 2 — ML Model
Trained an XGBoost regression model to predict position gain from a pit stop. Used SHAP to understand *why* it was making the predictions it was — not just what.

### Phase 3 — Tyre Degradation Model
This one was the most interesting to build. Lap-by-lap degradation modeled using compound, tyre age, and track conditions. Without this, the strategy engine would be guessing.

### Phase 4 — Strategy Engine
The simulation layer. Compares staying out vs. pitting, accounts for pit loss vs. degradation loss, and identifies undercut windows. This is where decisions actually get made.

### Phase 5 — Multi-Agent AI
Two agents working together: a **Strategy Agent** that makes the call, and an **Analyst Agent** that critiques and refines it. The goal was to get reasoning that holds up — not just confident-sounding text.

### Phase 6 — LangGraph Orchestration
Wired the agents into a stateful graph using LangGraph. This allowed for feedback loops — if the analyst flags something, the strategy agent can revise before the final output.

### Phase 7 — F1 Chatbot *(in progress)*
A conversational interface built with Ollama + LangChain that can answer F1-related questions. The plan is to connect it directly to the live strategy engine.

### Phase 8 — Dashboard & Real Data Integration ✅
The most visible part of the project. Replaced all simulated data with real telemetry via FastF1, and built a Streamlit dashboard with:
- Real lap times and speed plots
- ML-based degradation curves
- Dynamic driver selection
- Strategy simulation panel
- A cleaner UX that reacts instantly to driver changes

---

## What you can explore

**Telemetry Analysis** — Speed vs. distance, lap time trends, pulled from real race sessions.

**Performance Insights** — Average pace, degradation tracking, flagging which laps were critical.

**Strategy Engine** — Pit decision logic, undercut simulations, traffic-aware planning.

**Race Reports** — Structured summaries written in engineer-speak. Concise, no filler.

**Interactive Dashboard** — Everything above, in one place, with live inputs.

---

## Tech Stack

| Area | Tools |
|---|---|
| Core | Python |
| Data & ML | Pandas, NumPy, XGBoost, Scikit-learn, SHAP |
| F1 Data | FastF1 |
| AI & Agents | LangChain, LangGraph, Ollama |
| Visualization | Plotly, Streamlit |

---

## Project Structure

```
f1-ai-race-engineer/
├── analysis/
├── ml/
├── agents/
├── simulation/
├── dashboard/
├── src/
├── data/
└── README.md
```

---

## Running it locally

```bash
git clone <your-repo-link>
cd f1-ai-race-engineer
pip install -r requirements.txt
```

**Dashboard:**
```bash
streamlit run dashboard/app.py
```

**Race Simulation:**
```bash
python simulation/race_simulation.py
```

**Chatbot:**
```bash
python agents/f1_chatbot.py
```

---

## What's next

A few things I want to build out:

- Race outcome prediction (not just pit strategy, but where you'll finish)
- Multi-driver comparison within the same session
- A proper optimization layer for pit windows
- Real-time race ingestion during a live Grand Prix
- Web deployment with a React frontend + FastAPI backend

---

## The bigger picture

F1 strategy is one of the few domains where decisions worth millions of dollars get made in seconds, with incomplete information, under enormous pressure. 

This project is an attempt to formalize that process — combining data engineering, machine learning, simulation, and AI reasoning into something that actually thinks about races the way engineers do.

It's still a work in progress. But it's the most fun I've had building anything.

---

**Anubhab Pradhan**

---

*If this is the kind of thing you find interesting, a star on the repo goes a long way ⭐*