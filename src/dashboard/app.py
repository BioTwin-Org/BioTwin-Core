import streamlit as st
import pandas as pd
import plotly.express as px
from stmol import showmol
import py3Dmol
from src.model_containers.agent_based.liver_model import LiverModel
from src.generative.hormokine_designer import HormokineDesigner

st.set_page_config(page_title="BioTwin Spatial Engine", layout="wide")

if "model_a" not in st.session_state:
    st.session_state.model_a = LiverModel(size=50, fibrosis_level=0.7, genetic_risk=1.5)
    st.session_state.active_drug = None

# --- SIDEBAR ---
with st.sidebar:
    st.title("📂 Clinical Export")
    df_history = pd.DataFrame(st.session_state.model_a.history)
    if not df_history.empty:
        csv = df_history.to_csv(index=False).encode('utf-8')
        st.download_button("📥 DOWNLOAD CSV", data=csv, file_name="biotwin_spatial.csv")
    if st.button("♻️ RESET SYSTEM"):
        st.session_state.clear()
        st.rerun()

# --- MAIN INTERFACE ---
st.title("🔬 Digital Twin: Spatial Tissue Analysis")

col_ctrl, col_map, col_mol = st.columns([1, 2, 1.5])

with col_ctrl:
    st.subheader("Controls")
    if st.button("▶ Run Simulation Step", use_container_width=True):
        st.session_state.model_a.update_state()
    
    if st.button("💉 Inject Therapy", use_container_width=True):
        designer = HormokineDesigner()
        drug = designer.design_candidate("TGFBR2", "INHIBIT")
        st.session_state.active_drug = drug
        st.session_state.model_a.inject_hormokine(drug.instruction_potency, drug.predicted_affinity)

    st.markdown("---")
    st.metric("Tissue Viability", f"{st.session_state.model_a.viability*100:.1f}%")
    st.progress(st.session_state.model_a.toxicity, text="Toxicity Level")

with col_map:
    st.subheader("Spatial Distribution (Cellular Grid)")
    # Mapeo de colores: 0=Verde(Sano), 1=Marrón(Fibrosis), 2=Rojo(Inflamación)
    fig = px.imshow(
        st.session_state.model_a.grid,
        color_continuous_scale=[[0, 'green'], [0.5, 'brown'], [1, 'red']],
        labels=dict(color="Tissue State")
    )
    fig.update_coloraxes(showscale=False)
    fig.update_layout(width=500, height=500, margin=dict(l=10, r=10, b=10, t=10))
    st.plotly_chart(fig, use_container_width=True)

with col_mol:
    st.subheader("Molecular View")
    if st.session_state.active_drug:
        drug = st.session_state.active_drug
        view = py3Dmol.view(width=400, height=300)
        view.addModel(drug.structure.pdb_content, 'pdb')
        view.setStyle({'cartoon': {'color': 'spectrum'}})
        view.zoomTo()
        showmol(view, height=300, width=400)
