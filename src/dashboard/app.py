import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from stmol import showmol
import py3Dmol
from src.model_containers.agent_based.liver_model import LiverModel
from src.generative.hormokine_designer import HormokineDesigner
from src.generative.alpha_genome_service import AlphaGenomeService

st.set_page_config(page_title="BioTwin AI Explorer", layout="wide")

# Inicialización forzando el reseteo de llaves si hay error
if "model_a" not in st.session_state:
    st.session_state.model_a = LiverModel(size=50, fibrosis_level=0.6, genetic_risk=1.8)
    st.session_state.active_drug = None
    service = AlphaGenomeService()
    st.session_state.genotype = service.fetch_patient_profile("PT-2026-DX")

# --- SIDEBAR ---
with st.sidebar:
    st.title("Settings")
    st.info(f"Patient: {st.session_state.genotype}")
    target_select = st.selectbox("Target", ["TGFBR2", "IL-6R", "VEGFA", "PDGFR"])
    if st.button("♻️ RESET SYSTEM"):
        st.session_state.clear()
        st.rerun()

# --- MAIN ---
st.title("🔬 BioTwin: Spatial IA Discovery")
col_ctrl, col_map, col_mol = st.columns([1, 2, 1.5])

with col_ctrl:
    st.subheader("Controls")
    if st.button("▶ Run Step", use_container_width=True):
        st.session_state.model_a.update_state()
        st.rerun()
    
    # BOTÓN NORMAL
    if st.button("💉 Manual Injection", use_container_width=True):
        designer = HormokineDesigner()
        drug = designer.design_candidate(target_select, "INHIBIT", st.session_state.genotype)
        st.session_state.active_drug = drug
        st.session_state.model_a.inject_hormokine(drug.instruction_potency, drug.predicted_affinity)
        st.rerun()

    # NUEVO BOTÓN FASE B (IA)
    if st.button("🧬 AI AUTO-DISCOVERY", use_container_width=True, type="primary"):
        with st.spinner("IA Evolution in progress..."):
            designer = HormokineDesigner()
            # Optimizamos buscando la mejor de 5 variantes
            best_drug = designer.optimize_design(target_select, str(st.session_state.genotype))
            st.session_state.active_drug = best_drug
            st.session_state.model_a.inject_hormokine(best_drug.instruction_potency, best_drug.predicted_affinity)
            st.rerun()

    st.markdown("---")
    curr = st.session_state.model_a.get_status()
    # USAMOS .get() PARA EVITAR KEYERROR SIEMPRE
    viability_val = curr.get('Viability', 0)
    st.metric("Tissue Viability", f"{viability_val*100:.1f}%")
    st.progress(curr.get('Toxicity', 0), text="Safety Monitor")

with col_map:
    st.subheader("Spatial Grid")
    fig = px.imshow(st.session_state.model_a.grid, 
                    color_continuous_scale=[[0, '#2ecc71'], [0.5, '#8b4513'], [1, '#e74c3c']],
                    zmin=0, zmax=2)
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), height=400)
    st.plotly_chart(fig, use_container_width=True, key=f"grid_{st.session_state.model_a.step}")

with col_mol:
    st.subheader("Structure")
    if st.session_state.active_drug:
        drug = st.session_state.active_drug
        st.caption(f"Candidate: {drug.name}")
        view = py3Dmol.view(width=400, height=300)
        view.addModel(drug.structure.pdb_content, 'pdb')
        view.setStyle({'cartoon': {'color': 'spectrum'}})
        view.zoomTo()
        showmol(view, height=300, width=400)
