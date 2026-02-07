import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import time
import json
from stmol import showmol
import py3Dmol
from src.model_containers.agent_based.liver_model import LiverModel
from src.generative.hormokine_designer import HormokineDesigner

st.set_page_config(page_title="BioTwin AI Discovery", layout="wide", page_icon="🚀")

# --- LÓGICA DE CARGA DE DATOS ---
def load_patient_data(uploaded_file):
    if uploaded_file is not None:
        data = json.load(uploaded_file)
        return data
    return None

# --- SIDEBAR (ACTUALIZADA) ---
with st.sidebar:
    st.title("📂 Patient Data Portal")
    
    # Nuevo Uploader de archivos
    uploaded_file = st.file_uploader("Upload Genomic Profile (.json)", type=["json"])
    patient_data = load_patient_data(uploaded_file)
    
    if patient_data:
        st.success(f"Loaded: {patient_data['patient_id']}")
        st.json(patient_data)
        if st.button("🧬 INITIALIZE WITH PATIENT DATA"):
            st.session_state.model_a = LiverModel(
                size=50, 
                fibrosis_level=patient_data['initial_fibrosis'], 
                genetic_risk=patient_data['genotype_risk']
            )
            st.session_state.genotype = patient_data['patient_id']
            st.rerun()

    st.markdown("---")
    st.header("⚙️ Simulation Controls")
    target_select = st.selectbox("Select Target Receptor", ["TGFBR2", "IL-6R", "VEGFA", "PDGFR"])
    
    if st.button("♻️ RESET SYSTEM", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- MAIN LAYOUT ---
st.title("🧬 BioTwin Core: AI Auto-Discovery")

col_ctrl, col_map, col_mol = st.columns([1.2, 2, 1.5])

with col_ctrl:
    st.subheader("Discovery Engine")
    
    # IA AUTO-OPTIMIZE
    if st.button("🚀 IA AUTO-OPTIMIZE", type="primary", use_container_width=True):
        with st.status("IA screening candidates...") as status:
            designer = HormokineDesigner()
            # Generamos 5 opciones
            batch = designer.design_batch(target_select, "INHIBIT", st.session_state.genotype, n=5)
            # Selección de IA: Mejor (Potencia * Afinidad)
            best = max(batch, key=lambda d: d.instruction_potency * d.predicted_affinity)
            
            time.sleep(1)
            st.session_state.active_drug = best
            st.session_state.model_a.inject_hormokine(best.instruction_potency, best.predicted_affinity)
            status.update(label=f"Optimization Complete: {best.name}", state="complete")
    
    if st.button("▶ Run Simulation Step", use_container_width=True):
        st.session_state.model_a.update_state()

    st.markdown("---")
    curr = st.session_state.model_a.get_status()
    st.metric("Viability", f"{curr['Viability']*100:.1f}%")
    st.progress(curr['Toxicity'], text=f"Toxicity: {curr['Toxicity']*100:.1f}%")

with col_map:
    st.subheader("Spatial Tissue Map")
    # Generación del gráfico de tejido
    fig = px.imshow(
        st.session_state.model_a.grid,
        color_continuous_scale=[[0, '#2ecc71'], [0.5, '#8b4513'], [1, '#e74c3c']],
        zmin=0, 
        zmax=2
    )
    fig.update_coloraxes(showscale=False)
    fig.update_layout(height=450, margin=dict(l=0, r=0, b=0, t=0))
    st.plotly_chart(fig, use_container_width=True, key=f"grid_{st.session_state.model_a.step}")

with col_mol:
    st.subheader("Molecular Analysis")
    if st.session_state.active_drug:
        drug = st.session_state.active_drug
        st.markdown(f"**Candidate:** `{drug.name}`")
        view = py3Dmol.view(width=400, height=350)
        view.addModel(drug.structure.pdb_content, 'pdb')
        view.setStyle({'cartoon': {'color': 'spectrum'}})
        view.zoomTo()
        view.spin(True)
        showmol(view, height=350, width=400)
    else:
        st.info("Start AI Optimization to design protein.")
