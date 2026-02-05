import sys
import os

# --- PARCHE DE RUTAS ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import streamlit as st
import pandas as pd
import numpy as np
import time
from stmol import showmol
import py3Dmol

# Importaciones del Core
from src.model_containers.agent_based.liver_model import LiverModel
from src.generative.hormokine_designer import HormokineDesigner
from src.generative.alpha_genome_service import AlphaGenomeService

# Configuración de página
st.set_page_config(
    page_title="BioTwin Core | Endogenous Reprogramming",
    page_icon="🧬",
    layout="wide"
)

# --- SIDEBAR: Configuración del Paciente ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/dna-helix.png", width=60)
    st.title("BioTwin Controls")
    
    st.header("1. Genomic Stratification")
    st.info("Powered by AlphaGenome™")
    patient_id = st.text_input("Patient ID", "PT-2024-X99")
    
    genome_service = AlphaGenomeService()
    
    if "genotype" not in st.session_state:
        st.session_state.genotype = None

    if st.button("Analyze Genome"):
        with st.spinner("Sequencing variants..."):
            time.sleep(1)
            st.session_state.genotype = genome_service.fetch_patient_profile(patient_id)
            st.success("Profile Loaded")

    if st.session_state.genotype:
        risk = st.session_state.genotype.calculate_risk_factor()
        st.metric("Risk Factor", f"{risk}x", delta="High Risk" if risk > 1.2 else "Normal")
    
    st.markdown("---")
    st.header("2. BioNeMo Design")
    target = st.selectbox("Target Receptor", ["TGFBR2", "IL-6R", "EGFR"])
    action = st.radio("Mechanism", ["INHIBIT", "ACTIVATE"])

# --- MAIN PANEL ---
st.title("🧬 Digital Twin: Tissue Response Monitor")

col_sim, col_mol = st.columns([2, 1])

with col_sim:
    # Inicializar simulador
    if "model" not in st.session_state:
        g_risk = st.session_state.genotype.calculate_risk_factor() if st.session_state.genotype else 1.0
        st.session_state.model = LiverModel(fibrosis_level=0.75, genetic_risk=g_risk)

    c1, c2, c3 = st.columns(3)
    
    if c1.button("▶ Run Simulation Step"):
        st.session_state.model.update_state()
    
    if c2.button("💉 Inject Treatment"):
        designer = HormokineDesigner()
        candidate = designer.design_candidate(target, action, st.session_state.genotype)
        st.session_state.model.inject_hormokine(
            potency=candidate.instruction_potency, 
            target_affinity=candidate.predicted_affinity
        )
        st.session_state.last_drug = candidate
        st.toast(f"Treatment injected: {candidate.name}")

    if c3.button("🔄 Reset System"):
        for key in ["model", "last_drug"]:
            if key in st.session_state:
                st.session_state[key] = None
        st.rerun()

    # --- TELEMETRÍA Y GRÁFICOS ---
    # Línea 88 aprox: Aseguramos que el bloque tenga contenido
    if len(st.session_state.model.history) > 0:
        df = pd.DataFrame(st.session_state.model.history)
        
        # Selección segura de columnas
        available_cols = df.columns.tolist()
        plot_cols = ["Fibrosis", "Inflammation"]
        
        # Buscamos variaciones de 'Viability' para evitar el KeyError
        for v_name in ["Viability", "Hepatocyte Viability", "viability"]:
            if v_name in available_cols:
                plot_cols.append(v_name)
                break
        
        st.line_chart(df.set_index("Step")[plot_cols])
        
        # Métricas
        m1, m2, m3 = st.columns(3)
        curr = st.session_state.model.get_status()
        
        m1.metric("Fibrosis Index", f"{curr.get('fibrosis_index', 0):.2f}")
        m2.metric("Inflammation", f"{curr.get('inflammation_level', 0):.2f}")
        
        # Lógica de viabilidad para métrica
        v_val = curr.get('Viability') or curr.get('Hepatocyte Viability') or curr.get('viability', 0)
        m3.metric("Viability", f"{v_val:.2f}")
    else:
        st.info("Simulation engine ready. Click 'Run Simulation' to generate data.")

with col_mol:
    st.subheader("Molecular Analysis")
    if "last_drug" in st.session_state and st.session_state.last_drug:
        drug = st.session_state.last_drug
        st.write(f"**Candidate:** {drug.name}")
        
        if drug.structure and drug.structure.pdb_content:
            view = py3Dmol.view(width=400, height=400)
            view.addModel(drug.structure.pdb_content, 'pdb')
            view.setStyle({'cartoon': {'color': 'spectrum'}})
            view.zoomTo()
            showmol(view, height=400, width=400)
        else:
            st.warning("No PDB structure found.")
    else:
        st.info("Waiting for drug design sequences...")
