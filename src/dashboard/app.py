import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import time
from stmol import showmol
import py3Dmol

# Importaciones de lógica
from src.model_containers.agent_based.liver_model import LiverModel
from src.generative.hormokine_designer import HormokineDesigner

st.set_page_config(page_title="BioTwin AI Discovery", layout="wide", page_icon="🚀")

# --- ESTADO DE SESIÓN ---
if "model_a" not in st.session_state:
    st.session_state.model_a = LiverModel(size=50, fibrosis_level=0.7, genetic_risk=1.5)
    st.session_state.active_drug = None
    st.session_state.genotype = "High Risk (PNPLA3+)"

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("⚙️ Control Panel")
    target_select = st.selectbox("Select Target Receptor", ["TGFBR2", "IL-6R", "VEGFA", "PDGFR"])
    
    if st.button("♻️ RESET SYSTEM", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    
    st.markdown("---")
    df_h = pd.DataFrame(st.session_state.model_a.history)
    if not df_h.empty:
        st.download_button("📥 EXPORT CSV", data=df_h.to_csv().encode('utf-8'), file_name="ai_discovery.csv", use_container_width=True)

# --- PANEL PRINCIPAL ---
st.title("🧬 BioTwin Core: IA Auto-Discovery")

col_ctrl, col_map, col_mol = st.columns([1.2, 2, 1.5])

with col_ctrl:
    st.subheader("Discovery Engine")
    
    # --- EL BOTÓN AZUL (IA AUTO-OPTIMIZE) ---
    # Usamos type="primary" para forzar el color azul
    if st.button("🚀 IA AUTO-OPTIMIZE", use_container_width=True, type="primary"):
        with st.status("IA is screening candidates...") as status:
            designer = HormokineDesigner()
            # Generamos 5 candidatos
            candidates = designer.design_batch(target_select, "INHIBIT", st.session_state.genotype, n=5)
            
            # Algoritmo de Selección: $$Score = Potency \times Affinity$$
            best_drug = max(candidates, key=lambda d: d.instruction_potency * d.predicted_affinity)
            
            time.sleep(1) # Simulación de cómputo
            st.session_state.active_drug = best_drug
            st.session_state.model_a.inject_hormokine(best_drug.instruction_potency, best_drug.predicted_affinity)
            status.update(label=f"Best found: {best_drug.name}", state="complete")
            st.rerun()

    st.markdown("---")
    
    # Botón Secundario
    if st.button("💉 Manual Injection", use_container_width=True):
        designer = HormokineDesigner()
        drug = designer.design_candidate(target_select, "INHIBIT", st.session_state.genotype)
        st.session_state.active_drug = drug
        st.session_state.model_a.inject_hormokine(drug.instruction_potency, drug.predicted_affinity)
        st.rerun()

    if st.button("▶ Step Time", use_container_width=True):
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

with col_mol:
    st.subheader("Molecular Analysis")
    if st.session_state.active_drug:
        drug = st.session_state.active_drug
        st.markdown(f"**Current:** `{drug.name}`")
        view = py3Dmol.view(width=400, height=350)
        view.addModel(drug.structure.pdb_content, 'pdb')
        view.setStyle({'cartoon': {'color': 'spectrum'}})
        view.zoomTo()
        showmol(view, height=350, width=400)
    else:
        st.info("Trigger AI Optimization to design protein.")
