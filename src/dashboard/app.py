import streamlit as st
import pandas as pd
import time
from stmol import showmol
import py3Dmol
from src.model_containers.agent_based.liver_model import LiverModel
from src.generative.hormokine_designer import HormokineDesigner
from src.generative.alpha_genome_service import AlphaGenomeService

st.set_page_config(page_title="BioTwin Clinical Suite", layout="wide")

# --- LÓGICA DE EXPORTACIÓN ---
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

# --- SIDEBAR ---
with st.sidebar:
    st.title("Settings")
    mode = st.radio("Analysis Mode", ["Single Patient", "Patient Comparison (WT vs High Risk)"])
    patient_id = st.text_input("Patient ID", "PT-2024-X99")
    
    if st.button("Run Clinical Analysis"):
        st.session_state.analyzed = True
        st.success("Genomes Stratified")

# --- MAIN INTERFACE ---
st.title("🧬 BioTwin Core: Clinical Intelligence")

# Inicialización de modelos
if "model_1" not in st.session_state:
    st.session_state.model_1 = LiverModel(label="Patient A (High Risk)", genetic_risk=1.8)
    st.session_state.model_2 = LiverModel(label="Wild Type (Control)", genetic_risk=1.0)

col_ctrl, col_viz = st.columns([1, 2])

with col_ctrl:
    st.subheader("Controls")
    if st.button("▶ Run Step"):
        st.session_state.model_1.update_state()
        if mode != "Single Patient": st.session_state.model_2.update_state()
    
    if st.button("💉 Inject Therapy"):
        designer = HormokineDesigner()
        # Diseñamos para el objetivo seleccionado
        drug = designer.design_candidate("TGFBR2", "INHIBIT")
        st.session_state.last_drug = drug
        
        st.session_state.model_1.inject_hormokine(drug.instruction_potency, drug.predicted_affinity)
        if mode != "Single Patient":
            st.session_state.model_2.inject_hormokine(drug.instruction_potency, drug.predicted_affinity)
        st.toast("Therapy Administered")

    # BARRA DE TOXICIDAD (Nueva)
    st.markdown("---")
    st.subheader("Safety Monitor")
    tox = st.session_state.model_1.get_status()["Toxicity"]
    st.write(f"Toxicity Risk: {tox*100:.1f}%")
    st.progress(tox)
    if tox > 0.7: st.error("⚠️ HIGH TOXICITY ALERT")

with col_viz:
    # GRÁFICO COMPARATIVO
    df1 = pd.DataFrame(st.session_state.model_1.history)
    if mode != "Single Patient":
        df2 = pd.DataFrame(st.session_state.model_2.history)
        combined_df = pd.concat([df1, df2])
        st.line_chart(combined_df, x="Step", y="Fibrosis", color="Label")
    else:
        if not df1.empty:
            st.line_chart(df1.set_index("Step")[["Fibrosis", "Viability", "Toxicity"]])

# --- EXPORTADOR (Nuevo) ---
st.markdown("---")
if not df1.empty:
    st.subheader("📥 Export Clinical Data")
    csv = convert_df(df1)
    st.download_button(
        label="Download Simulation History (CSV)",
        data=csv,
        file_name=f"biotwin_report_{patient_id}.csv",
        mime="text/csv",
    )

# MOLECULAR VIEW (Mantener al final o en otra columna)
if "last_drug" in st.session_state:
    with st.expander("View Designed Molecule", expanded=True):
        view = py3Dmol.view(width=400, height=300)
        view.addModel(st.session_state.last_drug.structure.pdb_content, 'pdb')
        view.setStyle({'cartoon': {'color': 'spectrum'}})
        view.zoomTo()
        showmol(view, height=300, width=400)
