import streamlit as st
import pandas as pd
import time
import sys
import os

# Ensure Streamlit can find the project modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.generative.bionemo_client import BioNeMoClient
from src.model_containers.agent_based.liver_model import LiverLobule
from src.data_models.schemas import Hormokine

# Page Configuration
st.set_page_config(
    page_title="BioTwin Core | Research Dashboard",
    page_icon="🧬",
    layout="wide"
)

# Title and Header
st.title("🧬 BioTwin Core: Endogenous Reprogramming")
st.markdown("""
**Digital Twin Control Panel.** Design a custom Hormokine, simulate its injection into virtual tissue, 
and monitor the epigenetic response and fibrosis reversal in real-time.
""")

# --- SIDEBAR: HORMOKINE DESIGN (AI ENGINE) ---
st.sidebar.header("1. Generative Design (BioNeMo)")

target_receptor = st.sidebar.selectbox(
    "Target Receptor",
    ["TGFBR2 (Fibrosis Driver)", "EGFR (Regeneration)", "DOPAMINE_R (Off-target)"]
)

action_type = st.sidebar.selectbox(
    "Pharmacological Action",
    ["INHIBIT", "ACTIVATE"]
)

# Strip description for the logic
clean_receptor = target_receptor.split(" ")[0]

if st.sidebar.button("Generate Candidate"):
    with st.spinner("Connecting to BioNeMo Service..."):
        ai_client = BioNeMoClient()
        # The client now returns a structured Hormokine object
        candidate = ai_client.generate_hormokine(clean_receptor, action_type)
        st.session_state['candidate'] = candidate
        st.success("Hormokine Designed!")

# Display current candidate details
if 'candidate' in st.session_state:
    c = st.session_state['candidate']
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Active Molecule")
    st.sidebar.code(f"ID: {c.intervention_id}\nSequence: {c.sequence[:12]}...")
    st.sidebar.metric("Predicted Affinity", f"{c.predicted_affinity:.3f}")
    st.sidebar.metric("Instruction Potency", f"{c.instruction_potency:.2f}")

if 'candidate' in st.session_state:
    c = st.session_state['candidate']
    # Lógica del Semáforo de Seguridad
    if c.immunogenicity_score < 0.25:
        st.sidebar.success("✅ Safety Score: HIGH")
    elif c.immunogenicity_score < 0.45:
        st.sidebar.warning("⚠️ Safety Score: MEDIUM")
    else:
        st.sidebar.error("🚨 Safety Score: LOW (Toxic)")
    
    st.sidebar.progress(1.0 - c.immunogenicity_score) # Barra de salud de la molécula

# --- En el Panel de Métricas de Simulación (métrica m5) ---
with stats_placeholder.container():
    m1, m2, m3, m4, m5 = st.columns(5) # Añadimos una 5ta columna
    m1.metric("Step", f"{status['step']}")
    m2.metric("Fibrosis", f"{status['fibrosis_index']:.2f}", delta_color="inverse")
    m3.metric("Epigenetic", f"{status['epigenetic_status']:.2f}")
    m4.metric("Viability", f"{status['hepatocyte_viability']:.2f}")
    # Nueva métrica de Inmunogenicidad (Inversa para que 'positivo' sea bueno)
    m5.metric("Safety", f"{(1 - c.immunogenicity_score)*100:.0f}%")
    
# --- MAIN PANEL: SIMULATION (DIGITAL TWIN) ---
col1, col2 = st.columns([3, 1])

with col1:
    st.header("2. Physiological Simulation (LiverVerse)")
    
    start_sim = st.button("💉 Inject Treatment & Start Simulation", type="primary")
    
    chart_placeholder = st.empty()
    stats_placeholder = st.empty()

    if start_sim and 'candidate' in st.session_state:
        # Initialize Twin with severe fibrosis
        liver = LiverLobule(fibrosis_level=0.90)
        candidate = st.session_state['candidate']
        
        history = []
        progress_bar = st.progress(0)
        
        # Simulation Loop (30 Time Steps)
        for step in range(30):
            # Injection occurs at step 5
            if step == 5:
                st.toast(f"Injecting {candidate.intervention_id}...", icon="💉")
                liver.inject_treatment(candidate)
            else:
                liver.update_state()
            
            status = liver.get_status()
            history.append(status)
            
            # Update Dynamic Chart
            df = pd.DataFrame(history)
            # Reorganizing for better visualization
            chart_data = df.set_index('step')[['fibrosis_index', 'epigenetic_status', 'hepatocyte_viability']]
            
            chart_placeholder.line_chart(chart_data, height=400)
            
            # Update Metrics
            with stats_placeholder.container():
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Step", f"{status['step']}")
                m2.metric("Fibrosis Index", f"{status['fibrosis_index']:.2f}", delta_color="inverse")
                m3.metric("Epigenetic Driver", f"{status['epigenetic_status']:.2f}")
                m4.metric("Cell Viability", f"{status['hepatocyte_viability']:.2f}")

            time.sleep(0.1)
            progress_bar.progress((step + 1) / 30)
            
        st.success("Simulation Sequence Complete")

    elif start_sim:
        st.warning("Please generate a Hormokine in the sidebar first.")

with col2:
    st.header("Analytics")
    st.info("""
    **Legend:**
    * **Fibrosis Index (Blue):** Physical scarring of the tissue.
    * **Epigenetic Status (Orange):** Gene expression driver (Target for Reprogramming).
    * **Cell Viability (Green):** Overall hepatocyte health.
    """)
    
    with st.expander("Biological Logic Logs"):
        if 'candidate' in st.session_state:
            st.write(f"Targeting Receptor: {clean_receptor}")
            st.write(f"Action: {action_type}")
            st.write("Smart Release: Active (MMP-9 Sensor)")
        else:
            st.write("Waiting for data...")
