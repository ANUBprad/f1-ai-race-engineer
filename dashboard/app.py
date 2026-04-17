import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import plotly.graph_objects as go

from src.utils.config import setup_fastf1_cache
from src.data.data_loader import F1DataLoader

# Setup
setup_fastf1_cache()
loader = F1DataLoader()

st.set_page_config(page_title="F1 AI Engineer", layout="wide")

st.title(" F1 Telemetry Dashboard")

# Sidebar Inputs
year = st.sidebar.selectbox("Year", [2021, 2022, 2023, 2024])
gp = st.sidebar.text_input("Grand Prix", "Monza")
session_type = st.sidebar.selectbox("Session", ["R", "Q"])

driver = st.sidebar.text_input("Driver Code", "VER")
lap_number = st.sidebar.number_input("Lap Number", min_value=1, value=5)

# Load Session
if st.sidebar.button("Load Data"):

    with st.spinner("Loading session..."):
        session = loader.load_session(year, gp, session_type)

    st.success("Session loaded!")

    try:
        telemetry = loader.get_driver_telemetry(session, driver, lap_number)

        # Plot Speed
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=telemetry["Distance"],
            y=telemetry["Speed"],
            mode='lines',
            name='Speed'
        ))

        fig.update_layout(
            title=f"{driver} Lap {lap_number} Speed Trace",
            xaxis_title="Distance (m)",
            yaxis_title="Speed (km/h)",
            template="plotly_dark"
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")