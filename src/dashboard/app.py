import streamlit as st
import pandas as pd
from stmol import showmol
import py3Dmol
from src.model_containers.agent_based.liver_model import LiverModel
from src.generative.hormokine_designer import HormokineDesigner

# 1. Configuración de la Página
st.set_page_config(page_title="BioTwin Clinical Core", layout="wide", page_icon="🧬")

# 2. Inicialización del Estado
if "model_a" not in st.session_state:
    st.session_state.model_a = LiverModel(label="Patient High Risk (1.8x)", genetic_risk=1.8)
    st.session_state.active_drug = None

# --- BARRA LATERAL (Configuración y Exportación) ---
with st.sidebar:
    st.title("⚙️ Clinical Settings")
    
    if st.button("♻️ RESET SYSTEM", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    
    st.markdown("---")
    
    # --- SECCIÓN DE EXPORTACIÓN (CORREGIDA) ---
    st.subheader("📂 Data Export")
    
    # Obtenemos el historial
    df_history = pd.DataFrame(st.session_state.model_a.history)
    
    # Lógica robusta para el botón: Si hay datos, se muestra.
    if not df_history.empty:
        csv_data = df_history.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 DOWNLOAD REPORT (CSV)",
            data=csv_data,
            file_name="biotwin_clinical_report.csv",
            mime="text/csv",
            use_container_width=True,
            key="download_btn_sidebar" # Key única
        )
        st.caption(f"✅ {len(df_history)} records ready.")
    else:
        # Mensaje claro si no hay datos aún
        st.info("Run simulation to generate data for export.")

# --- INTERFAZ PRINCIPAL ---
st.title("🧬 BioTwin: Tissue Reprogramming Monitor")

col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("🕹️ Treatment Controls")
    
    if st.button("▶ Run Simulation Step", use_container_width=True):
        st.session_state.model_a.update_state()
    
    if st.button("💉 Inject Bio-Designed Therapy", use_container_width=True):
        with st.spinner("Designing & Folding Protein..."):
            designer = HormokineDesigner()
            # Alternamos el objetivo para dar variedad a la demostración
            target = "TGFBR2" if st.session_state.model_a.fibrosis > 0.5 else "IL-6R"
            drug = designer.design_candidate(target, "INHIBIT")
            st.session_state.active_drug = drug
            st.session_state.model_a.inject_hormokine(drug.instruction_potency, drug.predicted_affinity)
            st.toast(f"Therapy Administered: {drug.name}")

    st.markdown("---")
    
    # MONITOR DE TOXICIDAD
    st.subheader("⚠️ Toxicity Monitor")
    current_tox = st.session_state.model_a.toxicity
    st.progress(current_tox, text=f"Systemic Toxicity: {current_tox*100:.1f}%")
    
    if current_tox > 0.7:
        st.error("CRITICAL: High Toxicity Threshold Reached")
    elif current_tox > 0.3:
        st.warning("Warning: Moderate Side Effects")
    else:
        st.success("Safety Profile: Stable")

    # Métricas
    curr_status = st.session_state.model_a.get_status()
    c1, c2 = st.columns(2)
    c1.metric("Fibrosis", f"{curr_status['fibrosis_index']:.2f}")
    c2.metric("Viability", f"{curr_status['Viability']:.2f}")

with col_right:
    # GRÁFICO
    st.subheader("📈 Tissue Response Telemetry")
    if not df_history.empty:
        st.line_chart(
            df_history.set_index("Step")[["Fibrosis", "Viability", "Toxicity"]],
            height=300
        )
    
    # VISOR MOLECULAR 3D (ESTILO "ELEGANTE" RESTAURADO)
    st.subheader("🧬 Molecular Analysis")
    if st.session_state.active_drug:
        drug = st.session_state.active_drug
        
        # Configuración del visor para un look "premium"
        view = py3Dmol.view(width=600, height=400)
        view.addModel(drug.structure.pdb_content, 'pdb')
        view.setBackgroundColor('#0e1117') # Fondo oscuro
        
        # Estilo de cinta gruesa y coloreada (Cartoon Rainbow)
        view.setStyle({'cartoon': {'color': 'spectrum', 'thickness': 1.2}})
        
        # Añadimos una representación de "palitos" sutil para detalle atómico
        view.addStyle({'stick': {'radius': 0.15, 'opacity': 0.6, 'colorscheme': 'whiteCarbon'}})
        
        view.zoomTo()
        view.spin(True) # Animación de giro suave
        
        showmol(view, height=400, width=600)
        
        st.info(f"**Molecule:** {drug.name} | **Target:** {drug.target_receptor} | **Folding Score:** {drug.structure.plddt_score}%")
    else:
        st.info("Inject a treatment to visualize the designed protein structure.")       
