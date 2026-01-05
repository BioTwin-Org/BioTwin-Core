import streamlit as st
import pandas as pd
import time
import sys
import os

# Ensure Streamlit can find the project modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.generative.bionemo_client import BioNeMoClient
from src.model_containers.agent_based.liver_model import LiverLobule

# Page Configuration
st.set_page_config(
    page_title="BioTwin Core | Research Dashboard",
    page_icon="🧬",
    layout="wide"
)

# Custom CSS for better contrast
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# Title and Header
st.title("🧬 BioTwin Core: Endogenous Reprogramming")
st.markdown("""
**Digital Twin Framework.** Design synthetic Hormokines to silence pro-fibrotic drivers 
and reactivate regenerative pathways in human tissue.
""")

# --- SIDEBAR: HORMOKINE DESIGN ---
st.sidebar.header("1. Generative Design (AI)")

target_receptor = st.sidebar.selectbox(
    "Target Receptor",
    ["TGFBR2 (Stellate Cells)", "EGFR (Hepatocytes)", "DOPAMINE_R (Off-target)"]
)

action_type = st.sidebar.selectbox("Action", ["INHIBIT", "ACTIVATE"])

if st.sidebar.button("Generate Candidate"):
    with st.spinner("Connecting to BioNeMo AI..."):
        ai_client = BioNeMoClient()
        clean_target = target_receptor.split(" ")[0]
        candidate = ai_client.generate_hormokine(clean_target, action_type)
        st.session_state['candidate'] = candidate
        st.success("Hormokine Designed!")

# SAFETY SEMAPHORE & CANDIDATE INFO
if 'candidate' in st.session_state:
    c = st.session_state['candidate']
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Active Molecule Details")
    st.sidebar.code(f"ID: {c.intervention_id}\nSeq: {c.sequence[:12]}...")
    
    # Visual Safety Score logic
    if c.immunogenicity_score < 0.25:
        st.sidebar.success("✅ Safety: HIGH (Low Risk)")
    elif c.immunogenicity_score < 0.45:
        st.sidebar.warning("⚠️ Safety: MEDIUM")
    else:
        st.sidebar.error("🚨 Safety: LOW (Toxicity Risk)")
    
    st.sidebar.metric("Binding Affinity", f"{c.predicted_affinity:.2f}")

# --- MAIN PANEL: SIMULATION ---
col1, col2 = st.columns([3, 1])

with col1:
    st.header("2. Physiological Simulation (Multi-Agent)")
    start_sim = st.button("💉 Inject & Start Simulation", type="primary")
    
    chart_placeholder = st.empty()
    stats_placeholder = st.empty()

    if start_sim and 'candidate' in st.session_state:
        liver = LiverLobule(fibrosis_level=0.90)
        c = st.session_state['candidate']
        history = []
        
        # Simulation loop
        for step in range(40):
            if step == 5:
                st.toast(f"Injecting {c.intervention_id}...", icon="💉")
                liver.inject_treatment(c)
            else:
                liver.update_state()
            
            status = liver.get_status()
            history.append(status)
            
            # Dynamic Charting
            df = pd.DataFrame(history)
            chart_placeholder.line_chart(
                df.set_index('step')[['fibrosis_index', 'hsc_activation', 'hepatocyte_viability']],
                height=400
            )
            
            # Metrics Row - PERFECTLY INDENTED
            with stats_placeholder.container():
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Step", f"{status['step']}")
                m2.metric("Fibrosis", f"{status['fibrosis_index']:.2f}")
                m3.metric("HSC Activation", f"{status['hsc_activation']:.2f}", delta="-Inhibition")
                m4.metric("Cell Health", f"{status['hepatocyte_viability']:.2f}")
            
            time.sleep(0.05)

        # Post-Simulation Report
        st.success("Experiment Complete.")
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📊 Download Clinical Report (CSV)",
            data=csv_data,
            file_name=f"BioTwin_Report_{c.intervention_id}.csv",
            mime="text/csv"
        )

    elif start_sim:
        st.warning("Please generate a Hormokine in the sidebar before injecting.")

with col2:
    st.header("Bio-Intelligence")
    st.info("""
    **Legend:**
    * **Fibrosis (Blue):** ECM accumulation.
    * **HSC Activation (Orange):** The "Villain" cells causing scarring.
    * **Cell Health (Green):** Functional Hepatocyte viability.
    """)
    
    with st.expander("System Logs"):
        if 'candidate' in st.session_state:
            st.write(f"Candidate {c.intervention_id} is active.")
            st.write(f"Potency: {c.instruction_potency}")
        else:
            st.write("No active treatment detected.")        
