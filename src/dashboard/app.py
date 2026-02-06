import streamlit as st
import pandas as pd
from stmol import showmol
import py3Dmol
from src.model_containers.agent_based.liver_model import LiverModel
from src.generative.hormokine_designer import HormokineDesigner

st.set_page_config(page_title="BioTwin Clinical Core", layout="wide")

# Inicializar modelos si no existen
if "model_a" not in st.session_state:
    st.session_state.model_a = LiverModel(label="High Risk (1.8x)", genetic_risk=1.8)
    st.session_state.model_b = LiverModel(label="Wild Type (1.0x)", genetic_risk=1.0)
    st.session_state.active_drug = None

# --- SIDEBAR ---
with st.sidebar:
    st.header("🔬 Clinical Settings")
    mode = st.radio("Simulation Mode", ["Single Patient", "Comparison (High Risk vs WT)"])
    patient_id = st.text_input("Report ID", "REP-001")
    st.markdown("---")
    if st.button("♻️ Reset All Systems"):
        st.session_state.clear()
        st.rerun()

# --- MAIN VIEW ---
st.title("🧬 BioTwin: Clinical Reprogramming Monitor")

col_ctrl, col_chart, col_mol = st.columns([1, 2, 1.5])

with col_ctrl:
    st.subheader("Controls")
    if st.button("▶ Run Simulation Step", use_container_width=True):
        st.session_state.model_a.update_state()
        if mode == "Comparison (High Risk vs WT)": st.session_state.model_b.update_state()

    if st.button("💉 Inject Treatment", use_container_width=True):
        designer = HormokineDesigner()
        drug = designer.design_candidate("TGFBR2", "INHIBIT")
        st.session_state.active_drug = drug
        st.session_state.model_a.inject_hormokine(drug.instruction_potency, drug.predicted_affinity)
        if mode == "Comparison (High Risk vs WT)":
            st.session_state.model_b.inject_hormokine(drug.instruction_potency, drug.predicted_affinity)

    # MONITOR DE TOXICIDAD (Aparecerá aquí)
    st.markdown("---")
    st.subheader("⚠️ Safety Monitor")
    tox_val = st.session_state.model_a.toxicity
    st.progress(tox_val, text=f"Toxicity Level: {tox_val*100:.1f}%")
    if tox_val > 0.6: st.warning("High Toxicity Risk Detected")

with col_chart:
    st.subheader("Tissue Response Telemetry")
    df_a = pd.DataFrame(st.session_state.model_a.history)
    
    if mode == "Comparison (High Risk vs WT)":
        df_b = pd.DataFrame(st.session_state.model_b.history)
        combined = pd.concat([df_a, df_b])
        st.line_chart(combined, x="Step", y="Fibrosis", color="Label")
    else:
        if not df_a.empty:
            st.line_chart(df_a.set_index("Step")[["Fibrosis", "Viability", "Toxicity"]])

with col_mol:
    st.subheader("Molecular Analysis")
    if st.session_state.active_drug:
        drug = st.session_state.active_drug
        view = py3Dmol.view(width=400, height=300)
        view.addModel(drug.structure.pdb_content, 'pdb')
        view.setStyle({'cartoon': {'color': 'spectrum'}})
        view.zoomTo()
        showmol(view, height=300, width=400)
        st.caption(f"Target: {drug.target_receptor} | Seq: {drug.sequence[:20]}...")

# --- SECCIÓN DE DESCARGA (Exportador) ---
st.markdown("---")
if not df_a.empty:
    st.subheader("📥 Clinical Data Export")
    # Preparamos el CSV incluyendo la secuencia del fármaco si existe
    export_df = df_a.copy()
    if st.session_state.active_drug:
        export_df["Drug_Sequence"] = st.session_state.active_drug.sequence
    
    csv_data = export_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📩 Download Clinical Report (CSV)",
        data=csv_data,
        file_name=f"BioTwin_Report_{patient_id}.csv",
        mime="text/csv",
        use_container_width=True
    )
