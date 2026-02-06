import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from stmol import showmol
import py3Dmol
from src.model_containers.agent_based.liver_model import LiverModel
from src.generative.hormokine_designer import HormokineDesigner

st.set_page_config(page_title="BioTwin Spatial Engine", layout="wide")

# Inicialización con persistencia de historial
if "model_a" not in st.session_state:
    st.session_state.model_a = LiverModel(size=50, fibrosis_level=0.6, genetic_risk=1.2)
    st.session_state.active_drug = None

with st.sidebar:
    st.header("🧬 Stratification")
    # PERMITIMOS CAMBIAR EL TARGET PARA EVITAR REPETICIÓN
    target_select = st.selectbox("Target Receptor", ["TGFBR2", "IL-6R", "VEGFA", "PDGFR"])
    
    st.markdown("---")
    if st.button("♻️ RESET SYSTEM", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.title("🔬 Digital Twin: Spatial Tissue Analysis")

col_ctrl, col_map, col_mol = st.columns([1, 2, 1.5])

with col_ctrl:
    st.subheader("Controls")
    if st.button("▶ Run Simulation Step", use_container_width=True):
        st.session_state.model_a.update_state()
    
    if st.button("💉 Inject Therapy", use_container_width=True):
        with st.spinner("Designing Unique Candidate..."):
            designer = HormokineDesigner()
            # Usamos el target del selector de la sidebar
            drug = designer.design_candidate(target_select, "INHIBIT")
            st.session_state.active_drug = drug
            st.session_state.model_a.inject_hormokine(drug.instruction_potency, drug.predicted_affinity)

    st.markdown("---")
    curr = st.session_state.model_a.get_status()
    st.metric("Tissue Viability", f"{curr['Viability']*100:.1f}%")
    st.metric("Fibrosis Index", f"{curr['fibrosis_index']:.2f}")
    st.progress(curr['Toxicity'], text="Systemic Toxicity")

with col_map:
    st.subheader("Spatial Tissue Map")
    # Generamos el mapa con una clave de tiempo para forzar el refresco
    grid_data = st.session_state.model_a.grid
    fig = px.imshow(
        grid_data,
        color_continuous_scale=[[0, 'rgb(0, 255, 100)'], [0.5, 'rgb(139, 69, 19)'], [1, 'rgb(255, 50, 50)']],
        zmin=0, zmax=2
    )
    fig.update_coloraxes(showscale=False)
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), height=450)
    st.plotly_chart(fig, use_container_width=True, key=f"grid_{st.session_state.model_a.step}")

with col_mol:
    st.subheader("Molecular Design")
    if st.session_state.active_drug:
        drug = st.session_state.active_drug
        st.caption(f"**Candidate:** {drug.name}") # Aquí verás que el nombre ya cambia
        
        view = py3Dmol.view(width=400, height=350)
        view.addModel(drug.structure.pdb_content, 'pdb')
        view.setStyle({'cartoon': {'color': 'spectrum', 'thickness': 1.0}})
        view.zoomTo()
        view.spin(True)
        showmol(view, height=350, width=400)
        st.info(f"Affinity: {drug.predicted_affinity:.2f} | Confidence: {drug.structure.plddt_score}%")
    else:
        st.info("Waiting for drug design...")
