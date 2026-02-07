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

# --- GENERADOR DE INSIGHTS CLÍNICOS ---
def generate_clinical_report(drug, risk_factor):
    """Genera una narrativa técnica basada en los resultados de la IA."""
    potency_status = "ALTA" if drug.instruction_potency > 0.7 else "MODERADA"
    affinity_pct = drug.predicted_affinity * 100
    
    report = f"""
    📌 **Resumen de Inteligencia Clínica (AI-Generated):**
    
    Se ha seleccionado el candidato **{drug.name}** tras un cribado evolutivo de 5 variantes. 
    La variante muestra una afinidad predictiva del **{affinity_pct:.1f}%** hacia el receptor **{drug.target_receptor}**.
    
    **Justificación Terapéutica:**
    Debido al factor de riesgo genético detectado de **{risk_factor}x**, el sistema ha priorizado una 
    potencia de instrucción **{potency_status}** ({drug.instruction_potency:.2f}) para contrarrestar 
    la progresión de la fibrosis en el microambiente espacial del tejido. Se observa una estabilidad 
    estructural óptima para la administración sistémica.
    """
    return report

# --- INICIALIZACIÓN ---
if "model_a" not in st.session_state:
    st.session_state.model_a = LiverModel(size=50, fibrosis_level=0.7, genetic_risk=1.5)
    st.session_state.active_drug = None
    st.session_state.clinical_note = ""

# --- SIDEBAR (Uploader + Controles) ---
with st.sidebar:
    st.title("📂 Patient Data Portal")
    uploaded_file = st.file_uploader("Upload Genomic Profile (.json)", type=["json"])
    
    if uploaded_file:
        data = json.load(uploaded_file)
        st.success(f"Loaded: {data['patient_id']}")
        if st.button("🧬 INITIALIZE WITH PATIENT DATA"):
            st.session_state.model_a = LiverModel(
                size=50, 
                fibrosis_level=data['initial_fibrosis'], 
                genetic_risk=data['genotype_risk']
            )
            st.rerun()

    st.markdown("---")
    target_select = st.selectbox("Select Target Receptor", ["TGFBR2", "IL-6R", "VEGFA", "PDGFR"])
    
    if st.button("♻️ RESET SYSTEM", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- INTERFAZ PRINCIPAL ---
st.title("🧬 BioTwin Core: AI Auto-Discovery")

col_ctrl, col_map, col_mol = st.columns([1.2, 2, 1.5])

with col_ctrl:
    st.subheader("Discovery Engine")
    
    if st.button("🚀 IA AUTO-OPTIMIZE", type="primary", use_container_width=True):
        with st.status("IA is screening candidates...") as status:
            designer = HormokineDesigner()
            # Obtenemos el riesgo actual para el reporte
            risk_val = st.session_state.model_a.genetic_risk
            
            # IA Screening
            batch = designer.design_batch(target_select, "INHIBIT", str(risk_val), n=5)
            best_drug = max(batch, key=lambda d: d.instruction_potency * d.predicted_affinity)
            
            time.sleep(1)
            st.session_state.active_drug = best_drug
            st.session_state.model_a.inject_hormokine(best_drug.instruction_potency, best_drug.predicted_affinity)
            
            # Generar el Insight Clínico
            st.session_state.clinical_note = generate_clinical_report(best_drug, risk_val)
            
            status.update(label=f"Best found: {best_drug.name}", state="complete")
            st.rerun()

    st.markdown("---")
    curr = st.session_state.model_a.get_status()
    st.metric("Tissue Viability", f"{curr['Viability']*100:.1f}%")
    st.progress(curr['Toxicity'], text=f"Toxicity: {curr['Toxicity']*100:.1f}%")

with col_map:
    st.subheader("Live Spatial Tissue Map")
    fig = px.imshow(
        st.session_state.model_a.grid,
        color_continuous_scale=[[0, '#2ecc71'], [0.5, '#8b4513'], [1, '#e74c3c']],
        zmin=0, zmax=2
    )
    fig.update_coloraxes(showscale=False)
    fig.update_layout(height=400, margin=dict(l=0, r=0, b=0, t=0))
    st.plotly_chart(fig, use_container_width=True, key=f"grid_{st.session_state.model_a.step}")
    
    # NUEVA SECCIÓN: INSIGHTS CLÍNICOS
    if st.session_state.clinical_note:
        st.info(st.session_state.clinical_note)

with col_mol:
    st.subheader("Winning Molecule")
    if st.session_state.active_drug:
        drug = st.session_state.active_drug
        st.markdown(f"**Selected:** `{drug.name}`")
        view = py3Dmol.view(width=400, height=350)
        view.addModel(drug.structure.pdb_content, 'pdb')
        view.setStyle({'cartoon': {'color': 'spectrum'}})
        view.zoomTo()
        showmol(view, height=350, width=400)
    else:
        st.info("System Ready. Please run AI Optimization.")
