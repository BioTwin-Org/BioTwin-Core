import streamlit as st
import pandas as pd
import numpy as np
import py3Dmol
from stmol import showmol
import requests
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="BioTwin Core v2.0", layout="wide", initial_sidebar_state="expanded")

# --- ESTILOS CUSTOM (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 15px; border: 1px solid #30363d; }
    .stProgress > div > div > div > div { background-color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

# --- SERVICIOS MOCK / BIONEMO ---
class BioNeMoService:
    @staticmethod
    def get_real_cytokine_structure(pdb_id="1ALU"):
        """Obtiene la estructura 3D de la IL-6 (Interleucina-6)"""
        url = f"https://files.rcsb.org/view/{pdb_id}.pdb"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return {
                    "pdb": response.text,
                    "score": 94.2,
                    "weight": 21.0,
                    "name": "Interleukin-6 (IL-6)"
                }
        except:
            return None
        return None

# --- LÓGICA DEL MODELO (SIMULACIÓN ACTUALIZADA) ---
class LiverModel:
    def __init__(self):
        self.steps = 0
        self.fibrosis_level = 0.90
        self.hsc_activation_level = 1.0
        self.hepatocyte_viability = 0.40
        self.inflammation_level = 0.85 # Nivel inicial de daño
        self.history = []

    def inject_treatment(self, affinity):
        # Impacto de la Hormokina en la cascada inflamatoria
        reduction = affinity * 0.8
        self.inflammation_level = max(0.1, self.inflammation_level - reduction)
        self.hsc_activation_level = max(0.05, self.hsc_activation_level - (reduction * 1.2))
        return f"Injection Success: Inflammation reduced to {self.inflammation_level:.2f}"

    def update_state(self):
        self.steps += 1
        # Dinámica Kupffer -> HSC -> Fibrosis
        if self.inflammation_level > 0.4:
            self.hsc_activation_level = min(1.0, self.hsc_activation_level + 0.02)
        
        # Recuperación acelerada si el tratamiento funciona
        if self.hsc_activation_level < 0.45:
            self.fibrosis_level = max(0.0, self.fibrosis_level - 0.04)
            self.hepatocyte_viability = min(1.0, self.hepatocyte_viability + 0.01)
        else:
            self.fibrosis_level = min(1.0, self.fibrosis_level + 0.01)

        self.history.append({
            "Step": self.steps,
            "Fibrosis": self.fibrosis_level,
            "HSC_Activation": self.hsc_activation_level,
            "Inflammation": self.inflammation_level,
            "Cell_Health": self.hepatocyte_viability
        })

# --- FUNCIONES DE RENDERIZADO ---
def render_protein_3d(pdb_string):
    view = py3Dmol.view(width=400, height=300)
    view.addModel(pdb_string, 'pdb')
    view.setStyle({'cartoon': {'color': 'spectrum'}})
    view.addSurface(py3Dmol.VDW, {'opacity': 0.3, 'color': 'white'})
    view.zoomTo()
    view.spin(True)
    showmol(view, height=300, width=400)

# --- INICIALIZACIÓN DE ESTADO ---
if 'model' not in st.session_state:
    st.session_state.model = LiverModel()
    st.session_state.molecule = None

# --- SIDEBAR: GENERATIVE DESIGN ---
with st.sidebar:
    st.title("🧬 BioTwin Core AI")
    target = st.selectbox("Target Receptor", ["TGFBR2 (Stellate Cells)", "IL-6R (Kupffer Cells)"])
    action = st.radio("Action", ["INHIBIT", "ACTIVATE"])
    
    if st.button("Generate Hormokine"):
        with st.spinner("Consulting BioNeMo ESMFold..."):
            time.sleep(1)
            st.session_state.molecule = BioNeMoService.get_real_cytokine_structure()
            st.success("Candidate HK-5CE55878 Generated")

    if st.session_state.molecule:
        st.markdown("---")
        inf_color = "#ff4b4b" if st.session_state.model.inflammation_level > 0.5 else "#238636"
        st.markdown(f"""
            <div style="padding:10px; border-radius:10px; background-color:#161b22; border: 1px solid {inf_color};">
                <p style="margin:0; color:{inf_color}; font-size:12px;">KUPFFER POLARIZATION</p>
                <h3 style="margin:0;">{'M1 - INFLAMMATORY' if st.session_state.model.inflammation_level > 0.5 else 'M2 - REGENERATIVE'}</h3>
                <p style="margin:0; font-size:14px; color:#8b949e;">Cytokine Load: {st.session_state.model.inflammation_level:.2f}</p>
            </div>
        """, unsafe_allow_html=True)

# --- MAIN DASHBOARD ---
st.title("Digital Twin: Endogenous Reprogramming")
st.caption("Precision Medicine Simulation Framework | Liver Fibrosis Model")

col_main, col_viz = st.columns([2, 1])

with col_main:
    st.subheader("Physiological Telemetry")
    if st.button("💉 Inject & Start Simulation"):
        for _ in range(40):
            if st.session_state.model.steps == 5:
                st.session_state.model.inject_treatment(0.90)
            st.session_state.model.update_state()
            time.sleep(0.05)
        st.rerun()

    if st.session_state.model.history:
        df = pd.DataFrame(st.session_state.model.history)
        st.line_chart(df.set_index("Step")[["Fibrosis", "HSC_Activation", "Inflammation"]])

with col_viz:
    st.subheader("Molecular Structure")
    if st.session_state.molecule:
        render_protein_3d(st.session_state.molecule['pdb'])
        st.metric("pLDDT Confidence", f"{st.session_state.molecule['score']}%")
        st.caption(f"Structure: {st.session_state.molecule['name']}")
    else:
        st.info("Generate a candidate to view 3D structure")

# --- METRICS FOOTER ---
st.markdown("---")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Fibrosis Index", f"{st.session_state.model.fibrosis_level:.2f}", delta="-Reduction" if st.session_state.model.fibrosis_level < 0.5 else None)
m2.metric("HSC Activation", f"{st.session_state.model.hsc_activation_level:.2f}")
m3.metric("Inflammation", f"{st.session_state.model.inflammation_level:.2f}")
m4.metric("Hepatocyte Viability", f"{st.session_state.model.hepatocyte_viability:.2f}")

if st.button("Reset Simulation"):
    st.session_state.model = LiverModel()
    st.rerun()
