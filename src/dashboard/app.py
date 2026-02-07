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

if "model_a" not in st.session_state:
    st.session_state.model_a = LiverModel(size=50, fibrosis_level=0.7, genetic_risk=1.5)
    st.session_state.active_drug = None
    st.session_state.clinical_note = ""

with st.sidebar:
    st.title("📂 Patient Data")
    uploaded_file = st.file_uploader("Upload JSON", type=["json"])
    if uploaded_file:
        data = json.load(uploaded_file)
        if st.button("🧬 SYNC DIGITAL TWIN"):
            st.session_state.model_a = LiverModel(size=50, fibrosis_level=data['initial_fibrosis'], genetic_risk=data['genotype_risk'])
            st.rerun()
    st.markdown("---")
    st.subheader("📊 Export")
    df_history = pd.DataFrame(st.session_state.model_a.history)
    if not df_history.empty:
        st.download_button("📥 DOWNLOAD CSV", data=df_history.to_csv(index=False).encode('utf-8'), file_name="report.csv", mime="text/csv")
    st.markdown("---")
    target_select = st.selectbox("Target", ["TGFBR2", "IL-6R", "VEGFA", "PDGFR"])
    if st.button("♻️ RESET ALL"):
        st.session_state.clear()
        st.rerun()

st.title("🧬 BioTwin Core: AI Auto-Discovery")
col_ctrl, col_map, col_mol = st.columns([1.2, 2, 1.5])

with col_ctrl:
    st.subheader("Discovery Engine")
    if st.button("🚀 IA AUTO-OPTIMIZE", type="primary", use_container_width=True):
        with st.status("IA screening...") as status:
            designer = HormokineDesigner()
            risk_val = st.session_state.model_a.genetic_risk
            batch = designer.design_batch(target_select, "INHIBIT", risk_val, n=5)
            best_drug = max(batch, key=lambda d: d.instruction_potency * d.predicted_affinity)
            time.sleep(1)
            st.session_state.active_drug = best_drug
            st.session_state.model_a.inject_hormokine(best_drug.instruction_potency, best_drug.predicted_affinity)
            st.session_state.clinical_note = f"**Insight:** Seleccionado **{best_drug.name}** (Afinidad: {best_drug.predicted_affinity*100:.1f}%). Priorizado por riesgo de {risk_val}x."
            status.update(label=f"Optimized: {best_drug.name}", state="complete")
            st.rerun()
    if st.button("▶ Run Step", use_container_width=True):
        st.session_state.model_a.update_state()
        st.rerun()
    st.markdown("---")
    curr = st.session_state.model_a.get_status()
    st.metric("Tissue Viability", f"{curr['Viability']*100:.1f}%")
    st.progress(curr['Toxicity'], text=f"Toxicity: {curr['Toxicity']*100:.1f}%")

with col_map:
    st.subheader("Spatial Tissue Map")
    fig = px.imshow(
        st.session_state.model_a.grid,
        color_continuous_scale=[[0, '#2ecc71'], [0.5, '#8b4513'], [1, '#e74c3c']],
        zmin=0, zmax=2
    )
    fig.update_coloraxes(showscale=False)
    fig.update_layout(height=450, margin=dict(l=0, r=0, b=0, t=0))
    st.plotly_chart(fig, use_container_width=True, key=f"grid_{st.session_state.model_a.step}")
    if st.session_state.clinical_note:
        st.info(st.session_state.clinical_note)

with col_mol:
    st.subheader("Molecular Analysis")
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
        st.info("Start IA Optimization.")
