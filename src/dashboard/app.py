import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from stmol import showmol
import py3Dmol

# Importaciones de lógica interna
from src.model_containers.agent_based.liver_model import LiverModel
from src.generative.hormokine_designer import HormokineDesigner
from src.generative.alpha_genome_service import AlphaGenomeService

# 1. Configuración Global
st.set_page_config(page_title="BioTwin Core | Spatial & Clinical Suite", layout="wide", page_icon="🧬")

# 2. Inicialización de Estado de Sesión
if "model_a" not in st.session_state:
    # Iniciamos con un modelo espacial de 50x50 y riesgo genético alto
    st.session_state.model_a = LiverModel(size=50, fibrosis_level=0.6, genetic_risk=1.8)
    st.session_state.active_drug = None
    
    # Cargamos un genotipo inicial
    service = AlphaGenomeService()
    st.session_state.genotype = service.fetch_patient_profile("PT-2026-DX")

# --- BARRA LATERAL: Configuración y Exportación ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/dna-helix.png", width=60)
    st.title("Settings & Export")
    
    st.subheader("🧬 Stratification")
    st.info(f"Genotype: {st.session_state.genotype}")
    target_select = st.selectbox("Select Target Receptor", ["TGFBR2", "IL-6R", "VEGFA", "PDGFR"])
    
    st.markdown("---")
    
    # Exportador CSV
    st.subheader("📥 Clinical Report")
    df_history = pd.DataFrame(st.session_state.model_a.history)
    if not df_history.empty:
        csv = df_history.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="DOWNLOAD CSV REPORT",
            data=csv,
            file_name="biotwin_spatial_analysis.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    if st.button("♻️ RESET SYSTEM", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- PANEL PRINCIPAL ---
st.title("🔬 Digital Twin: Spatial Tissue Analysis")

col_ctrl, col_map, col_mol = st.columns([1, 2, 1.5])

# COLUMNA 1: Controles y Métricas
with col_ctrl:
    st.subheader("Controls")
    
    if st.button("▶ Run Simulation Step", use_container_width=True):
        st.session_state.model_a.update_state()
        st.rerun()
    
    if st.button("💉 Inject Therapy", use_container_width=True):
        with st.spinner("Designing Protein..."):
            designer = HormokineDesigner()
            # Pasamos Target, Mecanismo y el objeto Genotipo (corrigiendo el TypeError previo)
            drug = designer.design_candidate(target_select, "INHIBIT", st.session_state.genotype)
            st.session_state.active_drug = drug
            st.session_state.model_a.inject_hormokine(drug.instruction_potency, drug.predicted_affinity)
            st.rerun()

    st.markdown("---")
    curr = st.session_state.model_a.get_status()
    st.metric("Tissue Viability", f"{curr['viability']*100:.1f}%")
    
    st.subheader("⚠️ Toxicity Monitor")
    tox = curr['Toxicity']
    st.progress(tox, text=f"Level: {tox*100:.1f}%")
    if tox > 0.7: st.error("CRITICAL TOXICITY")

# COLUMNA 2: Mapa Espacial (Visualización de Tejido)
with col_map:
    st.subheader("Spatial Tissue Distribution")
    # Mapeo: 0=Sano (Verde), 1=Fibrosis (Marrón), 2=Inflamación (Rojo)
    grid_data = st.session_state.model_a.grid
    fig = px.imshow(
        grid_data,
        color_continuous_scale=[[0, '#2ecc71'], [0.5, '#8b4513'], [1, '#e74c3c']],
        zmin=0, zmax=2
    )
    fig.update_coloraxes(showscale=False)
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), height=450)
    st.plotly_chart(fig, use_container_width=True, key=f"spatial_step_{st.session_state.model_a.step}")
    st.caption("🟢 Healthy | 🟤 Fibrosis | 🔴 Inflammation")

# COLUMNA 3: Análisis Molecular 3D
with col_mol:
    st.subheader("Molecular Architecture")
    if st.session_state.active_drug:
        drug = st.session_state.active_drug
        st.markdown(f"**ID:** `{drug.name}`")
        st.markdown(f"**Target:** {drug.target_receptor}")
        
        view = py3Dmol.view(width=400, height=350)
        view.addModel(drug.structure.pdb_content, 'pdb')
        view.setStyle({'cartoon': {'color': 'spectrum', 'thickness': 1.0}})
        view.zoomTo()
        view.spin(True)
        showmol(view, height=350, width=400)
        st.info(f"Affinity: {drug.predicted_affinity:.2f} | Fold Score: {drug.structure.plddt_score}%")
    else:
        st.info("Please inject a therapy candidate to visualize protein folding.")

# GRÁFICA DE TENDENCIAS INFERIOR
st.markdown("---")
if not df_history.empty:
    st.subheader("📈 Temporal Evolution")
    st.line_chart(df_history.set_index("Step")[["Fibrosis", "Viability", "Toxicity"]], height=250)
