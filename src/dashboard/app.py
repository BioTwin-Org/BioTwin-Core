import streamlit as st
import pandas as pd
import plotly.express as px
import py3Dmol
from stmol import showmol
from src.model_containers.agent_based.liver_model import LiverModel
from src.generative.hormokine_designer import HormokineDesigner

st.set_page_config(page_title="BioTwin FIXED", layout="wide")

# Inicialización
if "model" not in st.session_state:
    st.session_state.model = LiverModel()
    st.session_state.drug = None

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("📂 Data & Config")
    target = st.selectbox("Target", ["TGFBR2", "IL-6R", "VEGFA"])
    
    st.markdown("---")
    # 1. BOTÓN DE DESCARGA (FORZADO)
    # Creamos datos dummy si está vacío para que el botón siempre aparezca
    data_to_save = st.session_state.model.history if st.session_state.model.history else [{"Step": 0, "Status": "Init"}]
    csv = pd.DataFrame(data_to_save).to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 DOWNLOAD CSV (Ready)",
        data=csv,
        file_name="biotwin_report.csv",
        mime="text/csv",
        use_container_width=True
    )

    if st.button("♻️ HARD RESET"):
        st.session_state.clear()
        st.rerun()

# --- MAIN ---
st.title("🔬 BioTwin: Final Repair")

# 2. GRÁFICA DE EVOLUCIÓN (MOVIDA ARRIBA)
# La ponemos arriba para verificar que se renderiza
if len(st.session_state.model.history) > 0:
    st.caption("📈 Live Metrics")
    hist_df = pd.DataFrame(st.session_state.model.history)
    st.line_chart(hist_df.set_index("Step")[["Viability", "Toxicity"]], height=200)

col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("Spatial Grid")
    # Mapa
    fig = px.imshow(st.session_state.model.grid, 
                    color_continuous_scale=[[0, '#00ff00'], [1, '#8b4513']],
                    zmin=0, zmax=1)
    fig.update_layout(margin=dict(l=0,r=0,b=0,t=0), height=400)
    st.plotly_chart(fig, use_container_width=True, key=f"map_{st.session_state.model.step}")
    
    # Controles
    c_a, c_b = st.columns(2)
    with c_a:
        if st.button("▶ Run Step", use_container_width=True):
            st.session_state.model.update_state()
            st.rerun()
    with c_b:
        if st.button("🧬 AI AUTO-DISCOVERY", type="primary", use_container_width=True):
            designer = HormokineDesigner()
            best = designer.optimize_design(target, "High Risk")
            st.session_state.drug = best
            st.session_state.model.inject_hormokine(best.instruction_potency, best.predicted_affinity)
            st.rerun()

with col2:
    st.subheader("3D Structure")
    if st.session_state.drug:
        d = st.session_state.drug
        st.info(f"Visualizing: {d.name}")
        
        # 3. VISUALIZADOR 3D SIMPLIFICADO
        # Usamos estilo 'stick' (palitos) que es más robusto si falla 'cartoon'
        view = py3Dmol.view(width=400, height=400)
        view.addModel(d.structure.pdb_content, 'pdb')
        view.setBackgroundColor('#0e1117')
        view.setStyle({'stick': {}})  # Cambiado a STICK para asegurar visibilidad
        view.zoomTo()
        showmol(view, height=400, width=400)
    else:
        st.warning("Click AI AUTO-DISCOVERY to generate protein.")
