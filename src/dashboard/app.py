import streamlit as st
import pandas as pd
import plotly.express as px
import json
import py3Dmol
from stmol import showmol
from src.model_containers.agent_based.liver_model import LiverModel
from src.generative.hormokine_designer import HormokineDesigner

st.set_page_config(page_title="BioTwin Final", layout="wide", page_icon="🧬")

# Inicialización
if "model" not in st.session_state:
    st.session_state.model = LiverModel()
    st.session_state.drug = None

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("📂 Data & Config")
    
    # 1. Cargador JSON
    up_file = st.file_uploader("Upload Patient JSON", type=["json"])
    if up_file:
        st.success("JSON Loaded")
    
    st.markdown("---")
    
    # 2. BOTÓN DE DESCARGA (Restaurado)
    # Creamos el DataFrame histórico
    history_data = st.session_state.model.history
    df = pd.DataFrame(history_data)
    
    # Botón siempre visible si hay datos
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 DOWNLOAD REPORT (CSV)",
        data=csv,
        file_name="biotwin_simulation_data.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.markdown("---")
    target = st.selectbox("Target", ["TGFBR2", "IL-6R", "VEGFA"])
    if st.button("♻️ RESET SYSTEM"):
        st.session_state.clear()
        st.rerun()

# --- PANEL PRINCIPAL ---
st.title("🔬 BioTwin: AI & Spatial Analysis")
c1, c2, c3 = st.columns([1, 2, 1.5])

with c1:
    st.subheader("Controls")
    if st.button("▶ Run Simulation Step", use_container_width=True):
        st.session_state.model.update_state()
        st.rerun()
    
    # Botón de IA
    if st.button("🧬 AI AUTO-DISCOVERY", type="primary", use_container_width=True):
        designer = HormokineDesigner()
        best = designer.optimize_design(target, "High Risk")
        st.session_state.drug = best
        st.session_state.model.inject_hormokine(best.instruction_potency, best.predicted_affinity)
        st.rerun()

    # Métricas
    curr = st.session_state.model.get_status()
    st.metric("Viability", f"{curr['Viability']*100:.1f}%")
    st.progress(min(1.0, curr['Toxicity']), text="Toxicity Monitor")

with c2:
    st.subheader("Spatial Grid")
    fig = px.imshow(st.session_state.model.grid, 
                    color_continuous_scale=[[0, '#00ff00'], [1, '#8b4513']],
                    zmin=0, zmax=1)
    fig.update_layout(margin=dict(l=0,r=0,b=0,t=0), height=400)
    st.plotly_chart(fig, use_container_width=True, key=f"g_{st.session_state.model.step}")

with c3:
    st.subheader("Molecular Architecture")
    if st.session_state.drug:
        d = st.session_state.drug
        st.markdown(f"**Candidate:** `{d.name}`")
        
        # VISOR 3D (Ajustado)
        view = py3Dmol.view(width=450, height=400)
        view.addModel(d.structure.pdb_content, 'pdb')
        view.setBackgroundColor('#0e1117')
        # Estilo grueso para visibilidad máxima
        view.setStyle({'cartoon': {'color': 'spectrum', 'thickness': 1.5}})
        view.zoomTo()
        view.spin(True)
        showmol(view, height=400, width=450)
    else:
        st.info("Waiting for AI Design...")

# --- GRÁFICA INFERIOR (Restaurada) ---
st.markdown("---")
st.subheader("📈 Temporal Evolution")
if not df.empty:
    # Mostramos las 3 métricas clave
    chart_data = df.set_index("Step")[["Viability", "Toxicity"]]
    st.line_chart(chart_data, height=300)
else:
    st.caption("Run simulation to see data trends.")
