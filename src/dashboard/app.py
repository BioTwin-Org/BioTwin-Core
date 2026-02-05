import sys
import os

# Agrega la raíz del proyecto al PATH de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Ahora sí, el resto de tus imports
import streamlit as st
from src.model_containers.agent_based.liver_model import LiverModel
import streamlit as st
import pandas as pd
import time
import py3Dmol
from stmol import showmol

# --- IMPORTACIONES DEL NÚCLEO ---
# Asegúrate de que las carpetas tengan su __init__.py
from src.model_containers.agent_based.liver_model import LiverModel
from src.generative.bionemo_service import BioNeMoService

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="BioTwin Core v2.0 | Liver Fibrosis",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🧬"
)

# --- ESTILOS CSS (Tema Cyber-Bio) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1, h2, h3 { color: #e6edf3; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 10px; }
    .stAlert { background-color: #161b22; color: #c9d1d9; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE ESTADO ---
if 'model' not in st.session_state:
    st.session_state.model = LiverModel()
if 'molecule' not in st.session_state:
    st.session_state.molecule = None

# --- SIDEBAR: GENOMICS & DESIGN ---
with st.sidebar:
    st.title("🧬 BioTwin Core")
    st.caption("v2.0.1-alpha | Powered by NVIDIA & DeepMind")
    
    # 1. Módulo AlphaGenome
    with st.expander("🧬 AlphaGenome: Patient Stratification", expanded=True):
        variant = st.selectbox(
            "Select Genomic Profile (SNP)",
            ["Wild Type (Standard)", "High Risk (IL6 rs1800795)", "Protective (TGFB1 rs1800470)"]
        )
        
        if variant == "High Risk (IL6 rs1800795)":
            st.session_state.model.genetic_risk = 1.4
            st.warning("⚠️ High Inflammatory Penetrance Detected")
        elif variant == "Protective (TGFB1 rs1800470)":
            st.session_state.model.genetic_risk = 0.7
            st.success("✅ Enhanced Regeneration Capacity")
        else:
            st.session_state.model.genetic_risk = 1.0

    # 2. Módulo BioNeMo
    st.markdown("---")
    st.subheader("🧪 BioNeMo Design")
    target = st.selectbox("Target Receptor", ["TGFBR2", "IL-6R", "PDGFR-beta"])
    
    if st.button("Generate Hormokine Candidate", use_container_width=True):
        service = BioNeMoService()
        with st.spinner("Folding protein sequence with ESMFold..."):
            time.sleep(1.5) # Simulación de latencia de red
            # Obtenemos estructura real (IL-6 1ALU para demo visual)
            st.session_state.molecule = service.get_real_cytokine_structure()
            st.success("Candidate HK-99X Folded Successfully")

    # Disclaimer Legal
    st.markdown("---")
    st.markdown("""
        <div style="font-size: 10px; color: #6e7681;">
            <b>LEGAL NOTICE:</b><br>
            Genomic analysis powered by AlphaGenome (DeepMind). 
            Weights used under CC-BY-NC 4.0 license. 
            Research use only. Not for clinical diagnosis.
        </div>
    """, unsafe_allow_html=True)

# --- PANEL PRINCIPAL ---
col_left, col_right = st.columns([2, 1])

with col_left:
    st.header("Endogenous Reprogramming Monitor")
    
    # Botón de Acción Principal
    start_sim = st.button("▶️ RUN SIMULATION / INJECT TREATMENT", type="primary")
    
    if start_sim:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Bucle de Simulación
        for i in range(50):
            # Inyectar tratamiento en el paso 10
            if i == 10 and st.session_state.molecule:
                st.session_state.model.inject_hormokine(potency=0.95, target_affinity=0.98)
                status_text.success("💉 TREATMENT INJECTED: Targeting IL-6/TGF-b Pathway")
            
            st.session_state.model.update_state()
            progress_bar.progress((i + 1) / 50)
            time.sleep(0.05)
            
        status_text.info("Simulation Complete")

    # Gráficos en tiempo real
    if len(st.session_state.model.history) > 0:
        df = pd.DataFrame(st.session_state.model.history)
        
        # Selección segura de columnas
        cols = ["Fibrosis", "Inflammation"]
        if "Viability" in df.columns:
            cols.append("Viability")
        elif "Hepatocyte Viability" in df.columns:
            cols.append("Hepatocyte Viability")

        st.line_chart(df.set_index("Step")[cols])
        
        # --- SECCIÓN DE MÉTRICAS 
        m1, m2, m3 = st.columns(3)
        curr = st.session_state.model.get_status()  # Esta línea debe estar alineada con m1, m2, m3
        
        m1.metric("Fibrosis Index", f"{curr['fibrosis_index']:.2f}")
        m2.metric("Inflammation", f"{curr['inflammation_level']:.2f}")
        
        # Verificación para la tercera métrica
        v_key = 'Viability' if 'Viability' in curr else 'hepatocyte_viability'
        m3.metric("Viability", f"{curr.get(v_key, 0):.2f}")

with col_right:
    st.subheader("Structural Biology (3D)")
    
    if st.session_state.molecule:
        # 1. Visor 3D
        pdb_data = st.session_state.molecule.get('pdb', '')
        view = py3Dmol.view(width=400, height=350)
        view.addModel(pdb_data, 'pdb')
        view.setStyle({'cartoon': {'color': 'spectrum'}})
        view.addSurface(py3Dmol.VDW, {'opacity': 0.3, 'color': 'white'})
        view.zoomTo()
        view.spin(True)
        showmol(view, height=350, width=400)
        
        st.caption(f"Structure: {st.session_state.molecule.get('name')} | pLDDT: {st.session_state.molecule.get('score')}")

        # 2. Indicador de Estado Inflamatorio (Kupffer)
        inf_val = st.session_state.model.inflammation_level
        is_inflamed = inf_val > 0.4
        
        state_color = "#ff4b4b" if is_inflamed else "#238636"
        state_text = "M1 - PRO-INFLAMMATORY" if is_inflamed else "M2 - REGENERATIVE"
        
        st.markdown(f"""
            <div style="margin-top: 20px; padding: 15px; border: 2px solid {state_color}; border-radius: 10px; background-color: #0d1117;">
                <strong style="color: {state_color};">KUPFFER CELL POLARIZATION</strong>
                <h3 style="margin: 5px 0; color: white;">{state_text}</h3>
                <div style="background: #30363d; width: 100%; height: 8px; border-radius: 4px;">
                    <div style="background: {state_color}; width: {min(100, inf_val*100)}%; height: 8px; border-radius: 4px; transition: width 0.5s;"></div>
                </div>
                <small style="color: #8b949e;">Cytokine Load Index: {inf_val:.2f}</small>
            </div>
        """, unsafe_allow_html=True)
        
    else:
        st.info("👈 Generate a molecule to enable 3D Analysis")
        # Placeholder visual
        st.markdown("""
            <div style="height: 300px; border: 1px dashed #30363d; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #8b949e;">
                Waiting for BioNeMo Output...
            </div>
        """, unsafe_allow_html=True)
