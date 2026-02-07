import streamlit as st
import pandas as pd
import plotly.express as px
import json
from stmol import showmol
import py3Dmol
from src.model_containers.agent_based.liver_model import LiverModel
from src.generative.hormokine_designer import HormokineDesigner

st.set_page_config(page_title="BioTwin AI Explorer", layout="wide")

# --- LÓGICA DE CARGA JSON ---
def load_patient_json(uploaded_file):
    if uploaded_file is not None:
        data = json.load(uploaded_file)
        st.sidebar.success(f"Loaded: {data.get('patient_name', 'Unknown')}")
        return data
    return None

# Inicialización
if "model_a" not in st.session_state:
    st.session_state.model_a = LiverModel(size=50, fibrosis_level=0.6, genetic_risk=1.5)
    st.session_state.active_drug = None

# --- SIDEBAR ---
with st.sidebar:
    st.title("Settings & Data")
    
    # NUEVO: Botón para cargar JSON
    uploaded_file = st.file_uploader("Upload Patient JSON", type=["json"])
    patient_data = load_patient_json(uploaded_file)
    
    st.markdown("---")
    target_select = st.selectbox("Select Target", ["TGFBR2", "IL-6R", "VEGFA", "PDGFR"])
    
    if st.button("♻️ RESET SYSTEM", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- MAIN INTERFACE ---
st.title("🔬 Digital Twin: Spatial Tissue Analysis")

col_ctrl, col_map, col_mol = st.columns([1, 2, 1.5])

with col_ctrl:
    st.subheader("Controls")
    if st.button("▶ Run Simulation Step", use_container_width=True):
        st.session_state.model_a.update_state()
    
    # Botón AI Discovery (Fase B)
    if st.button("🧬 AI AUTO-DISCOVERY", use_container_width=True, type="primary"):
        designer = HormokineDesigner()
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
    fig = px.imshow(st.session_state.model_a.grid, 
                    color_continuous_scale=[[0, '#2ecc71'], [0.5, '#8b4513'], [1, '#e74c3c']],
                    zmin=0, zmax=2)
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), height=400)
    st.plotly_chart(fig, use_container_width=True, key=f"grid_{st.session_state.model_a.step}")

with col_mol:
    st.subheader("Molecular Architecture")
    if st.session_state.active_drug:
        drug = st.session_state.active_drug
        st.markdown(f"**ID:** `{drug.name}`")
        
        # REPARACIÓN DE HELICOIDES: Forzamos el renderizado en el cuadro
        view = py3Dmol.view(width=400, height=350)
        view.addModel(drug.structure.pdb_content, 'pdb')
        # Estilo Ribbon/Cartoon para que se vea la hélice elegante
        view.setStyle({'cartoon': {'color': 'spectrum'}})
        view.zoomTo()
        view.spin(True)
        showmol(view, height=350, width=400)
        st.caption(f"Affinity: {drug.predicted_affinity:.2f} | Fold Score: {drug.structure.plddt_score}%")
    else:
        st.info("Inject therapy to visualize protein.")
