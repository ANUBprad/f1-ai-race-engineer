import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from src.utils.config import setup_fastf1_cache
from src.data.data_loader import F1DataLoader

from analysis.report_generator import generate_insights, generate_report
from ml.strategy_engine import StrategyEngine


# =========================
# SETUP
# =========================
setup_fastf1_cache()
loader = F1DataLoader()

st.set_page_config(page_title="F1 Race Engineer", layout="wide")

st.title("🏁 F1 Race Engineer")
st.caption("Telemetry • Strategy • Performance Analysis")


# =========================
# SIDEBAR INPUTS
# =========================
st.sidebar.header("Race Inputs")

year = st.sidebar.selectbox("Year", [2021, 2022, 2023, 2024])
gp = st.sidebar.text_input("Grand Prix", "Monza")
session_type = st.sidebar.selectbox("Session", ["R", "Q"])
lap_number = st.sidebar.number_input("Lap Number", min_value=1, value=5)

st.sidebar.markdown("---")
st.sidebar.subheader("Strategy Inputs")

compound = st.sidebar.selectbox("Tyre Compound", ["SOFT", "MEDIUM", "HARD"])
gap_ahead = st.sidebar.slider("Gap Ahead (s)", 0, 20, 5)
gap_behind = st.sidebar.slider("Gap Behind (s)", 0, 30, 20)

st.sidebar.markdown("---")
st.sidebar.subheader("Strategy Engine")
run_strategy = st.sidebar.button("Run Strategy")


# =========================
# LOAD SESSION (AUTO)
# =========================
with st.spinner("Loading session..."):
    session = loader.load_session(year, gp, session_type)

st.success("Session loaded")


# =========================
# DRIVER SELECTION
# =========================
driver_dict = {
    d: session.get_driver(d)["FullName"]
    for d in session.drivers
}

driver = st.selectbox(
    "Driver",
    list(driver_dict.keys()),
    format_func=lambda x: driver_dict[x]
)


# =========================
# SESSION CONTEXT
# =========================
st.markdown("### Session Context")

c1, c2, c3 = st.columns(3)
c1.metric("Driver", driver_dict[driver])
c2.metric("Grand Prix", gp)
c3.metric("Lap", lap_number)


# =========================
# TELEMETRY
# =========================
telemetry = loader.get_driver_telemetry(session, driver, lap_number)


# =========================
# REAL LAP TIMES
# =========================
lap_times = loader.get_lap_times(session, driver)
lap_times = lap_times[-10:]

if len(lap_times) < 3:
    st.warning("Not enough lap data for analysis")
    st.stop()


# =========================
# ML DEGRADATION
# =========================
engine = StrategyEngine()

degradation = [
    engine.predict_degradation(compound, i)
    for i in range(len(lap_times))
]

data = {
    "lap_times": lap_times,
    "degradation": degradation
}

insights = generate_insights(data)


# =========================
# LAYOUT
# =========================
col_main, col_side = st.columns([3, 1])


# =========================
# TELEMETRY GRAPH
# =========================
with col_main:
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=telemetry["Distance"],
        y=telemetry["Speed"],
        mode='lines',
        name='Speed'
    ))

    fig.update_layout(
        title=f"{driver} Lap {lap_number} Speed Trace",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    # LAP TIME TREND
    fig2 = px.line(
        x=list(range(len(lap_times))),
        y=lap_times,
        labels={"x": "Lap", "y": "Lap Time (s)"},
        title="Lap Time Evolution (Last 10 Laps)"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # DEGRADATION GRAPH
    fig3 = px.line(
        x=list(range(len(degradation))),
        y=degradation,
        labels={"x": "Lap", "y": "Degradation"},
        title="Tyre Degradation Curve"
    )

    st.plotly_chart(fig3, use_container_width=True)


# =========================
# INSIGHTS PANEL
# =========================
with col_side:
    st.subheader("Performance Insights")

    st.metric("Avg Lap Time", f"{round(insights['avg_lap_time'],2)} s")

    trend_map = {
        "increasing": "Performance dropping",
        "stable": "Consistent pace"
    }
    st.metric("Trend", trend_map.get(insights["trend"], insights["trend"]))

    st.metric("Degradation", round(insights["max_degradation"],2))
    st.metric("Critical Lap", insights["critical_lap"])

    try:
        position = session.laps.pick_drivers(driver)["Position"].iloc[-1]
        st.metric("Position", int(position))
    except:
        pass


# =========================
# STRATEGY (SEPARATE)
# =========================
if run_strategy:

    strategy = engine.decide(
        compound=compound,
        tyre_age=len(lap_times),
        circuit=gp,
        gap_ahead=gap_ahead,
        gap_behind=gap_behind
    )

    # STRATEGY COMPARISON
    stay_loss = engine.simulate_stay_out(compound, len(lap_times))
    pit_loss = engine.simulate_pit(gp)

    st.markdown("### Strategy Comparison")

    c1, c2 = st.columns(2)
    c1.metric("Stay Out Loss", f"{round(stay_loss, 2)} s")
    c2.metric("Pit Loss", f"{round(pit_loss, 2)} s")

    st.caption("Decision based on degradation vs pit loss comparison")

    st.markdown("### Strategy Assessment")

    if "PIT" in strategy["action"]:
        st.error(strategy["action"])
    else:
        st.success(strategy["action"])

    st.progress(strategy["confidence"])
    st.caption(f"Confidence: {round(strategy['confidence']*100)}%")

    with st.expander("Reasoning"):
        st.write(strategy["reasoning"])

    # =========================
    # 🔥 NEW: STRATEGY SIMULATION
    # =========================
    st.markdown("### Strategy Simulation")

    sim = engine.simulate_strategy_options(
        compound=compound,
        tyre_age=len(lap_times),
        circuit=gp,
        gap_ahead=gap_ahead
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Stay Out Loss", f"{sim['stay_out_loss']} s")
    col2.metric("Pit Loss", f"{sim['pit_loss']} s")
    col3.metric("Undercut Gain", f"{sim['undercut_gain']} s")

    fig_sim = px.bar(
        x=["Stay Out", "Pit", "Undercut"],
        y=[
            sim["stay_out_loss"],
            sim["pit_loss"],
            sim["undercut_gain"]
        ],
        title="Strategy Outcome Comparison"
    )

    st.plotly_chart(fig_sim, use_container_width=True)

    # REPORT WITH STRATEGY
    report = generate_report(insights, strategy)

else:
    report = generate_report(insights, {"action": "HOLD", "confidence": 0})


# =========================
# REPORT
# =========================
st.markdown("### Race Summary")

sections = report.split("\n\n")
for section in sections:
    st.markdown(section)


# =========================
# FOOTNOTE
# =========================
st.caption("Note: Analysis based on recent laps and ML-based degradation model")