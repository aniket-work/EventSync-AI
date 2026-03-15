import streamlit as st
from agents import create_graph
import pandas as pd

st.set_page_config(page_title="EventSync-AI Dashboard", layout="wide")

st.title("🤝 EventSync-AI: Human-in-the-Loop Orchestrator")
st.markdown("### Corporate Event Logistics Simulation")

if 'state' not in st.session_state:
    st.session_state.state = {
        "messages": [],
        "plan": {"location": "New York City", "attendee_count": 200, "budget_limit": 25000},
        "budget_total": 18200.0,
        "confirmed_items": [
            {"venue": {"name": "Grand Plaza Hotel", "price_per_day": 5000, "rating": 4.8}},
            {"catering": {"vendor": "Elite Gourmet", "total_cost": 15000, "rating": 4.9}}
        ],
        "approval_required": True,
        "final_report": ""
    }

col1, col2 = st.columns(2)

with col1:
    st.subheader("Event Configuration")
    st.json(st.session_state.state["plan"])
    
    st.subheader("Budget Analysis")
    st.metric("Total Estimated Cost", f"${st.session_state.state['budget_total']}")
    if st.session_state.state["budget_total"] > 15000:
        st.warning("⚠️ Budget threshold exceeded. Explicit approval required.")

with col2:
    st.subheader("Proposed Vendors")
    df = pd.DataFrame([
        {"Item": "Venue", "Name": "Grand Plaza Hotel", "Cost": "$5000", "Rating": 4.8},
        {"Item": "Catering", "Name": "Elite Gourmet", "Cost": "$15000", "Rating": 4.9}
    ])
    st.table(df)
    
    if st.button("Confirm and Execute Contracts"):
        st.success("✅ Contracts Executed! Check terminal for logs.")
        st.balloons()

st.sidebar.markdown("---")
st.sidebar.info("This is an experimental PoC for agentic event management.")
