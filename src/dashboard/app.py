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

# Title and Header
st.title("🧬 BioTwin Core: Endogenous Reprogramming")
st.markdown("Digital Twin Control Panel for Epigenetic Tissue Programming.")

# --- SIDEBAR: HORMOKINE DESIGN ---
st.sidebar.header("1. Generative Design")

target_receptor = st.sidebar.selectbox(
    "Target Receptor",
    ["TGFBR2 (Fibrosis)", "EGFR (Regeneration)", "DOPAMINE_R (Off-target)"]
)

action_type = st.sidebar.selectbox("Action", ["INHIBIT", "ACTIVATE"])

if st.sidebar.button("Generate Candidate"):
    with st.spinner("Designing via BioNeMo..."):
        ai_client = BioNeMoClient()
        clean_target = target_receptor.split(" ")[0]
        candidate = ai_client.generate_hormokine(clean_target, action_type)
        st.session_state['candidate'] = candidate
        st.success("Hormokine Designed!")

# SAFETY SEMAPHORE LOGIC
if 'candidate' in st.session_state:
    c = st.session_state['candidate']
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Active Molecule")
    st.sidebar.code(f"ID: {c.intervention_id}\nSeq: {c.sequence[:12]}...")
    
    # Visual Safety Score
    if c.immunogenicity_score < 0.25:
        st.sidebar.success("✅ Safety: HIGH")
    elif c.immunogenicity_score < 0.45:
        st.sidebar.warning("⚠️ Safety: MEDIUM")
    else:
        st.sidebar.error("🚨 Safety: LOW (Toxic)")
    
    st.sidebar.metric("Affinity", f"{c.predicted_affinity:.2f}")

# --- MAIN PANEL: SIMULATION ---
col1, col2 = st.columns([3, 1])

with col1:
    st.header("2. Physiological Simulation")
    start_sim = st.button("💉 Start Treatment", type="primary")
    
    chart_placeholder = st.empty()
    stats_placeholder = st.empty()

    if start_sim and 'candidate' in st.session_state:
        liver = LiverLobule(fibrosis_level=0.90)
        c = st.session_state['candidate']
        history = []
        
        for step in range(30):
            if step == 5:
                st.toast(f"Injecting {c.intervention_id}...", icon="💉")
                liver.inject_treatment(c)
            else:
                liver.update_state()
            
            status = liver.get_status()
            history.append(status)
            
            df = pd.DataFrame(history)
            chart_placeholder.line_chart(df.set_index('step')[['fibrosis_index', 'epigenetic_status', 'hepatocyte_viability']])
            
            with stats_placeholder.container():
                m1, m2, m3, m4, m5 = st.columns(5)
                m1.metric("Step", f"{status['step']}")
                m2.metric("Fibrosis", f"{status['fibrosis_index']:.2f}")
                m3.metric("Epigenetic", f"{status['epigenetic_status']:.2f}")
                m4.metric("Viability", f"{status['hepatocyte_viability']:.2f}")
                m5.metric("Safety", f"{(1 - c.immunogenicity_score)*100:.0f}%")
            time.sleep(0.05)
# --- NUEVA LÓGICA DE REPORTE ---
        st.success("Simulation Sequence Complete")
        
        # Generar CSV a partir de la historia
        csv_data = df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📊 Download Clinical Simulation Report (CSV)",
            data=csv_data,
            file_name=f"BioTwin_Report_{c.intervention_id}.csv",
            mime="text/csv",
            help="Click to download the full time-series data of this experiment."
        )

        # Mostrar tabla de datos opcional
        with st.expander("View Raw Data Table"):
            st.dataframe(df)
with col2:
    st.header("Analytics")
    st.info("Monitor how the instruction domain affects the epigenetic driver.")
