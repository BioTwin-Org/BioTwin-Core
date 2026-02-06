import streamlit as st
import pandas as pd
from stmol import showmol
import py3Dmol
from src.model_containers.agent_based.liver_model import LiverModel
from src.generative.hormokine_designer import HormokineDesigner

st.set_page_config(page_title="BioTwin Clinical", layout="wide")

# Forzar la creación de modelos nuevos
if "model_a" not in st.session_state or st.sidebar.button("♻️ RESET SYSTEM"):
    st.session_state.model_a = LiverModel(label="Patient High Risk", genetic_risk=1.8)
    st.session_state.active_drug = None
    st.session_state.step_count = 0

# --- BARRA LATERAL (Exportador Aquí) ---
with st.sidebar:
    st.title("📂 Clinical Export")
    df_history = pd.DataFrame(st.session_state.model_a.history)
    if not df_history.empty:
        csv = df_history.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 DOWNLOAD CSV REPORT",
            data=csv,
            file_name="biotwin_clinical_report.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("Run simulation to enable download")

# --- CUERPO PRINCIPAL ---
st.title("🧬 BioTwin: Tissue Reprogramming Monitor")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Controls")
    if st.button("▶ Run Simulation Step"):
        st.session_state.model_a.update_state()
    
    if st.button("💉 Inject Treatment"):
        designer = HormokineDesigner()
        drug = designer.design_candidate("TGFBR2", "INHIBIT")
        st.session_state.active_drug = drug
        st.session_state.model_a.inject_hormokine(drug.instruction_potency, drug.predicted_affinity)

    st.markdown("---")
    st.subheader("⚠️ Toxicity Monitor")
    tox = st.session_state.model_a.toxicity
    st.progress(tox, text=f"Level: {tox*100:.1f}%")

with col2:
    if not df_history.empty:
        st.line_chart(df_history, x="Step", y=["Fibrosis", "Viability", "Toxicity"])
        
        # Visor 3D
        if st.session_state.active_drug:
            view = py3Dmol.view(width=400, height=300)
            view.addModel(st.session_state.active_drug.structure.pdb_content, 'pdb')
            view.setStyle({'cartoon': {'color': 'spectrum'}})
            view.zoomTo()
            showmol(view, height=300, width=400)    
