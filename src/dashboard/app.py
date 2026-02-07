import streamlit as st
import pandas as pd
import plotly.express as px
import json
import py3Dmol
from stmol import showmol
from src.model_containers.agent_based.liver_model import LiverModel
from src.generative.hormokine_designer import HormokineDesigner

st.set_page_config(page_title="BioTwin AI Explorer", layout="wide", page_icon="🔬")

# --- FUNCIONES DE CARGA ---
def load_patient_data(file):
    if file:
        return json.load(file)
    return None

# --- INICIALIZACIÓN ---
if "model_a" not in st.session_state:
    st.session_state.model_a = LiverModel(size=50, fibrosis_level=0.6, genetic_risk=1.5)
    st.session_state.active_drug = None

# --- BARRA LATERAL (Fase C) ---
with st.sidebar:
    st.title("📂 Patient Data")
    
    # Botón para cargar JSON
    uploaded_file = st.file_uploader("Upload Patient Genomic JSON", type=["json"])
    if uploaded_file:
        data = load_patient_data(uploaded_file)
        st.success(f"Loaded: {data.get('patient_id', 'Unknown')}")
        st.json(data) # Previsualización rápida

    st.markdown("---")
    target_select = st.selectbox("Select Target Receptor", ["TGFBR2", "IL-6R", "VEGFA", "PDGFR"])
    
    if st.button("♻️ RESET SYSTEM", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- PANEL PRINCIPAL ---
st.title("🔬 Digital Twin: Spatial & AI Discovery")

col_ctrl, col_map, col_mol = st.columns([1, 2, 1.5])

with col_ctrl:
    st.subheader("Controls")
    if st.button("▶ Run Simulation Step", use_container_width=True):
        st.session_state.model_a.update_state()
    
    # BOTÓN FASE B (IA)
    if st.button("🧬 AI AUTO-DISCOVERY", use_container_width=True, type="primary"):
        with st.spinner("IA Evolutionary Loop..."):
            designer = HormokineDesigner()
            # La IA busca el mejor candidato automáticamente
            best_drug = designer.optimize_design(target_select, "High Risk")
            st.session_state.active_drug = best_drug
            st.session_state.model_a.inject_hormokine(best_drug.instruction_potency, best_drug.predicted_affinity)
            st.rerun()

    st.markdown("---")
    curr = st.session_state.model_a.get_status()
    st.metric("Tissue Viability", f"{curr.get('Viability', 0)*100:.1f}%")
    st.progress(curr.get('Toxicity', 0), text=f"Toxicity: {curr.get('Toxicity', 0)*100:.1f}%")

with col_map:
    st.subheader("Spatial Tissue Distribution")
    # Mapa de calor de 50x50 píxeles
    fig = px.imshow(st.session_state.model_a.grid, 
                    color_continuous_scale=[[0, '#2ecc71'], [0.5, '#8b4513'], [1, '#e74c3c']],
                    zmin=0, zmax=2)
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), height=400)
    st.plotly_chart(fig, use_container_width=True, key=f"spatial_grid_{st.session_state.model_a.step}")
    st.caption("🟢 Healthy | 🟤 Fibrosis | 🔴 Inflammation")

with col_mol:
    st.subheader("Molecular Architecture")
    if st.session_state.active_drug:
        drug = st.session_state.active_drug
        st.markdown(f"**Candidate:** `{drug.name}`")
        
        # --- FIX VISOR 3D (Hélices Elegantes) ---
        view = py3Dmol.view(width=400, height=350)
        view.addModel(drug.structure.pdb_content, 'pdb')
        # Fondo oscuro para resaltar el arcoíris
        view.setBackgroundColor('#0e1117') 
        # Estilo Ribbon/Cartoon grueso
        view.setStyle({'cartoon': {'color': 'spectrum', 'thickness': 1.0}})
        view.zoomTo()
        view.spin(True)
        showmol(view, height=350, width=400)
    else:
        st.info("System Standby. Initiate AI Discovery or Manual Injection.")
