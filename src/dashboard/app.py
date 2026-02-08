import streamlit as st
import pandas as pd
import plotly.express as px
import py3Dmol
from stmol import showmol
from src.model_containers.agent_based.liver_model import LiverModel
from src.generative.hormokine_designer import HormokineDesigner

st.set_page_config(page_title="BioTwin Final", layout="wide")

# Inicialización
if "model" not in st.session_state:
    st.session_state.model = LiverModel()
    st.session_state.drug = None

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🧬 Configuration")
    
    # 1. Cargador JSON
    up_file = st.file_uploader("Upload Patient JSON", type=["json"])
    if up_file:
        st.success("JSON Loaded")
    
    st.markdown("---")
    
    # 2. SELECCIÓN DE OBJETIVO Y MECANISMO (NUEVO)
    target = st.selectbox("Target Receptor", ["TGFBR2", "IL-6R", "VEGFA"])
    mechanism = st.radio("Mechanism of Action", ["INHIBIT", "ACTIVATE"])
    
    st.markdown("---")
    
    # 3. RESET
    if st.button("♻️ RESET SIMULATION", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- PANEL PRINCIPAL ---
st.title("🔬 BioTwin: AI Tissue Engineering")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Spatial Tissue Analysis")
    # Mapa de calor
    fig = px.imshow(st.session_state.model.grid, 
                    color_continuous_scale=[[0, '#00ff00'], [1, '#8b4513']],
                    zmin=0, zmax=1)
    fig.update_layout(margin=dict(l=0,r=0,b=0,t=0), height=450)
    st.plotly_chart(fig, use_container_width=True, key=f"map_{st.session_state.model.step}")
    
    # Controles de Simulación
    c_a, c_b = st.columns(2)
    with c_a:
        if st.button("▶ Run Simulation Step", use_container_width=True):
            st.session_state.model.update_state()
            st.rerun()
    with c_b:
        # Botón IA
        if st.button(f"🧬 AI AUTO-DISCOVERY ({mechanism})", type="primary", use_container_width=True):
            designer = HormokineDesigner()
            # Pasamos el mecanismo seleccionado
            best = designer.optimize_design(target, mechanism, "High Risk")
            st.session_state.drug = best
            st.session_state.model.inject_hormokine(best.instruction_potency, best.predicted_affinity)
            st.rerun()
            
    # Métricas rápidas
    curr = st.session_state.model.get_status()
    st.metric("Current Viability", f"{curr['Viability']*100:.1f}%", delta=f"{curr['Viability']*10:.1f}%")

with col2:
    st.subheader("Molecular Architecture")
    if st.session_state.drug:
        d = st.session_state.drug
        st.markdown(f"**Candidate:** `{d.name}`")
        st.markdown(f"**Action:** `{d.mechanism}` | **Affinity:** `{d.predicted_affinity:.2f}`")
        
        # VISOR 3D
        view = py3Dmol.view(width=400, height=400)
        view.addModel(d.structure.pdb_content, 'pdb')
        view.setBackgroundColor('#0e1117')
        view.setStyle({'stick': {}, 'cartoon': {'color': 'spectrum'}})
        view.zoomTo()
        showmol(view, height=400, width=400)
        
        # BOTÓN DE DESCARGA PDB (NUEVO)
        st.download_button(
            label="📥 DOWNLOAD STRUCTURE (.PDB)",
            data=d.structure.pdb_content,
            file_name=f"{d.name}.pdb",
            mime="chemical/x-pdb",
            use_container_width=True
        )
    else:
        st.info("Run AI Discovery to generate a candidate.")

# --- GRÁFICA INFERIOR (CLARA Y RESTAURADA) ---
st.markdown("---")
st.subheader("📈 Clinical Evolution Report")

if len(st.session_state.model.history) > 0:
    hist_df = pd.DataFrame(st.session_state.model.history)
    
    # Gráfica de líneas grande
    chart = st.line_chart(hist_df.set_index("Step")[["Viability", "Toxicity"]], height=350)
    
    # Botón de descarga CSV
    csv = hist_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📄 Download Clinical Data (CSV)",
        data=csv,
        file_name="biotwin_clinical_data.csv",
        mime="text/csv"
    )
else:
    st.warning("Start the simulation to verify data trends.")
