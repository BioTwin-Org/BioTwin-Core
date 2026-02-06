import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from stmol import showmol
import py3Dmol
from src.model_containers.agent_based.liver_model import LiverModel
from src.generative.hormokine_designer import HormokineDesigner

st.set_page_config(page_title="BioTwin Spatial Engine", layout="wide")

# 1. Estado de Sesión
if "model_a" not in st.session_state:
    st.session_state.model_a = LiverModel(size=50, fibrosis_level=0.6, genetic_risk=1.5)
    st.session_state.active_drug = None
    st.session_state.genotype = "High Risk (1.8x)"

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🧬 Patient Stratification")
    st.info(f"Current Genotype: {st.session_state.genotype}")
    target_select = st.selectbox("Select Target Receptor", ["TGFBR2", "IL-6R", "VEGFA", "PDGFR"])
    
    st.markdown("---")
    if st.button("♻️ RESET SYSTEM", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    
    # Exportador
    df_h = pd.DataFrame(st.session_state.model_a.history)
    if not df_h.empty:
        csv = df_h.to_csv(index=False).encode('utf-8')
        st.download_button("📥 DOWNLOAD CSV REPORT", data=csv, file_name="spatial_report.csv", use_container_width=True)

# --- INTERFAZ PRINCIPAL ---
st.title("🔬 Digital Twin: Spatial Tissue Analysis")

col_ctrl, col_map, col_mol = st.columns([1, 2, 1.5])

with col_ctrl:
    st.subheader("Controls")
    if st.button("▶ Run Simulation Step", use_container_width=True):
        st.session_state.model_a.update_state()
    
    if st.button("💉 Inject Therapy", use_container_width=True):
        with st.spinner("Designing Candidate..."):
            designer = HormokineDesigner()
            # LLAMADA CORREGIDA: 3 argumentos (target, mechanism, genotype)
            drug = designer.design_candidate(target_select, "INHIBIT", st.session_state.genotype)
            st.session_state.active_drug = drug
            st.session_state.model_a.inject_hormokine(drug.instruction_potency, drug.predicted_affinity)

    st.markdown("---")
    curr = st.session_state.model_a.get_status()
    st.metric("Tissue Viability", f"{curr['Viability']*100:.1f}%")
    st.progress(curr['Toxicity'], text=f"Toxicity: {curr['Toxicity']*100:.1f}%")

with col_map:
    st.subheader("Live Spatial Tissue Map")
    # Mostrar el grid con colores: Verde(0), Marrón(1), Rojo(2)
    fig = px.imshow(
        st.session_state.model_a.grid,
        color_continuous_scale=[[0, '#2ecc71'], [0.5, '#8b4513'], [1, '#e74c3c']],
        zmin=0, zmax=2
    )
    fig.update_coloraxes(showscale=False)
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), height=450)
    st.plotly_chart(fig, use_container_width=True, key=f"spatial_grid_{st.session_state.model_a.step}")

with col_mol:
    st.subheader("Molecular Architecture")
    if st.session_state.active_drug:
        drug = st.session_state.active_drug
        st.markdown(f"**ID:** `{drug.name}`")
        
        view = py3Dmol.view(width=400, height=350)
        view.addModel(drug.structure.pdb_content, 'pdb')
        view.setStyle({'cartoon': {'color': 'spectrum'}})
        view.zoomTo()
        view.spin(True)
        showmol(view, height=350, width=400)
    else:
        st.info("System Ready. Please inject treatment.")
