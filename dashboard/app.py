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
# LOAD SESSION
# =========================
with st.spinner("Loading session..."):
    session = loader.load_session(year, gp, session_type)

st.success("Session loaded")


# =========================
# DRIVER SELECTION (MULTI)
# =========================
driver_dict = {
    d: session.get_driver(d)["FullName"]
    for d in session.drivers
}

drivers_selected = st.multiselect(
    "Select Drivers (Max 2)",
    list(driver_dict.keys()),
    default=[list(driver_dict.keys())[0]]
)

if len(drivers_selected) == 0:
    st.warning("Select at least one driver")
    st.stop()

if len(drivers_selected) > 2:
    st.warning("Select maximum 2 drivers")
    st.stop()


# =========================
# SESSION CONTEXT
# =========================
st.markdown("### Session Context")

c1, c2, c3 = st.columns(3)
c1.metric("Grand Prix", gp)
c2.metric("Session", session_type)
c3.metric("Lap", lap_number)


engine = StrategyEngine()


# =========================
# SINGLE DRIVER MODE
# =========================
if len(drivers_selected) == 1:

    driver = drivers_selected[0]

    st.subheader(f"{driver_dict[driver]} — Performance Overview")

    telemetry = loader.get_driver_telemetry(session, driver, lap_number)

    lap_times = loader.get_lap_times(session, driver)[-10:]

    if len(lap_times) < 3:
        st.warning("Not enough lap data")
        st.stop()

    degradation = [
        engine.predict_degradation(compound, i)
        for i in range(len(lap_times))
    ]

    data = {
        "lap_times": lap_times,
        "degradation": degradation
    }

    insights = generate_insights(data)

    col_main, col_side = st.columns([3, 1])

    # =========================
    # GRAPH
    # =========================
    with col_main:
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=telemetry["Distance"],
            y=telemetry["Speed"],
            mode='lines'
        ))

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig, use_container_width=True)

        # Lap trend
        fig2 = px.line(
            x=list(range(len(lap_times))),
            y=lap_times,
            title="Lap Time Evolution"
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Degradation
        fig3 = px.line(
            x=list(range(len(degradation))),
            y=degradation,
            title="Tyre Degradation Curve"
        )
        st.plotly_chart(fig3, use_container_width=True)

    # =========================
    # INSIGHTS
    # =========================
    with col_side:
        st.subheader("Performance Insights")

        st.metric("Avg Lap", f"{round(insights['avg_lap_time'],2)} s")
        st.metric("Trend", insights["trend"])
        st.metric("Degradation", round(insights["max_degradation"],2))
        st.metric("Critical Lap", insights["critical_lap"])

    # =========================
    # STRATEGY
    # =========================
    if run_strategy:

        strategy = engine.decide(
            compound=compound,
            tyre_age=len(lap_times),
            circuit=gp,
            gap_ahead=gap_ahead,
            gap_behind=gap_behind
        )

        st.markdown("### Strategy Assessment")

        if "PIT" in strategy["action"]:
            st.error(strategy["action"])
        else:
            st.success(strategy["action"])

        st.progress(strategy["confidence"])

        # Simulation
        st.markdown("### Strategy Simulation")

        sim = engine.simulate_strategy_options(
            compound=compound,
            tyre_age=len(lap_times),
            circuit=gp,
            gap_ahead=gap_ahead
        )

        st.write(sim)

        # What-if
        st.markdown("### What-If")

        if st.button("Simulate Pit Now"):

            stay = engine.simulate_stay_out(compound, len(lap_times))
            pit = engine.simulate_pit(gp)

            delta = stay - pit

            if delta > 0:
                st.success(f"Pit now gains ~{round(delta,2)}s")
            else:
                st.warning(f"Pit now loses ~{round(abs(delta),2)}s")

        report = generate_report(insights, strategy)

    else:
        report = generate_report(insights, {"action": "HOLD", "confidence": 0})

    # REPORT
    st.markdown("### Race Summary")
    st.markdown(report)


# =========================
# MULTI DRIVER MODE
# =========================
else:

    d1, d2 = drivers_selected

    st.subheader("Driver Comparison")

    laps1 = loader.get_lap_times(session, d1)[-10:]
    laps2 = loader.get_lap_times(session, d2)[-10:]

    fig_compare = px.line(
        x=list(range(len(laps1))),
        y=[laps1, laps2],
        title="Pace Comparison"
    )

    st.plotly_chart(fig_compare, use_container_width=True)

    avg1 = round(sum(laps1)/len(laps1), 2)
    avg2 = round(sum(laps2)/len(laps2), 2)

    c1, c2 = st.columns(2)

    c1.metric(driver_dict[d1], f"{avg1} s")
    c2.metric(driver_dict[d2], f"{avg2} s")

    faster = d1 if avg1 < avg2 else d2
    st.success(f"{driver_dict[faster]} has better pace")


# =========================
# FOOTNOTE
# =========================
st.caption("Analysis based on telemetry and ML-driven degradation model")