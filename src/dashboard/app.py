import streamlit as st
import pandas as pd
from stmol import showmol
import py3Dmol
from src.model_containers.agent_based.liver_model import LiverModel
from src.generative.hormokine_designer import HormokineDesigner

# 1. Configuración de la Página
st.set_page_config(page_title="BioTwin Clinical Core", layout="wide", page_icon="🧬")

# 2. Inicialización del Estado (Singleton Pattern)
if "model_a" not in st.session_state:
    # Inicializamos con un paciente de Alto Riesgo por defecto
    st.session_state.model_a = LiverModel(label="Patient High Risk (1.8x)", genetic_risk=1.8)
    st.session_state.active_drug = None

# --- BARRA LATERAL (Configuración y Exportación) ---
with st.sidebar:
    st.title("⚙️ Clinical Settings")
    
    # Botón de Reinicio Total
    if st.button("♻️ RESET SYSTEM", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    
    st.markdown("---")
    
    # SECCIÓN DE EXPORTACIÓN (Mejorada)
    st.subheader("📂 Data Export")
    
    # Obtenemos el historial actual
    df_history = pd.DataFrame(st.session_state.model_a.history)
    
    # El botón aparece siempre que haya datos (incluso solo el inicial)
    if not df_history.empty:
        csv_data = df_history.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 DOWNLOAD REPORT (CSV)",
            data=csv_data,
            file_name="biotwin_clinical_report.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.caption(f"Records available: {len(df_history)}")
    else:
        st.warning("No data to export yet.")

# --- INTERFAZ PRINCIPAL ---
st.title("🧬 BioTwin: Tissue Reprogramming Monitor")

# Dividimos en dos columnas: Controles+Métricas vs Gráficos+3D
col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("🕹️ Treatment Controls")
    
    # Botón de Simulación de Tiempo
    if st.button("▶ Run Simulation Step", use_container_width=True):
        st.session_state.model_a.update_state()
    
    # Botón de Inyección (Generativa)
    if st.button("💉 Inject Bio-Designed Therapy", use_container_width=True):
        with st.spinner("Designing Protein Structure..."):
            designer = HormokineDesigner()
            drug = designer.design_candidate("TGFBR2", "INHIBIT")
            st.session_state.active_drug = drug
            st.session_state.model_a.inject_hormokine(drug.instruction_potency, drug.predicted_affinity)
            st.success("Therapy Administered")

    st.markdown("---")
    
    # MONITOR DE TOXICIDAD (Mejorado)
    st.subheader("⚠️ Toxicity Monitor")
    current_tox = st.session_state.model_a.toxicity
    
    # Color dinámico de la barra según gravedad
    bar_color = "red" if current_tox > 0.7 else "blue"
    st.progress(current_tox, text=f"Systemic Toxicity: {current_tox*100:.1f}%")
    
    if current_tox > 0.7:
        st.error("CRITICAL: High Toxicity Threshold Reached")
    elif current_tox > 0.3:
        st.warning("Warning: Moderate Side Effects")
    else:
        st.success("Safety Profile: Stable")

    # Métricas numéricas rápidas
    curr_status = st.session_state.model_a.get_status()
    c1, c2 = st.columns(2)
    c1.metric("Fibrosis", f"{curr_status['fibrosis_index']:.2f}")
    c2.metric("Viability", f"{curr_status['Viability']:.2f}")

with col_right:
    # GRÁFICO DE TELEMETRÍA
    st.subheader("📈 Tissue Response Telemetry")
    if not df_history.empty:
        # Mostramos Fibrosis, Viabilidad y Toxicidad
        st.line_chart(
            df_history.set_index("Step")[["Fibrosis", "Viability", "Toxicity"]],
            height=300
        )
    
    # VISOR MOLECULAR 3D
    st.subheader("🧬 Molecular Analysis")
    if st.session_state.active_drug:
        drug = st.session_state.active_drug
        
        # Configuración visual para ver hélices (Cartoon Rainbow)
        view = py3Dmol.view(width=600, height=400)
        view.addModel(drug.structure.pdb_content, 'pdb')
        view.setBackgroundColor('#0e1117') # Fondo oscuro integrado
        
        # Estilo principal: Cinta coloreada por espectro
        view.setStyle({'cartoon': {'color': 'spectrum'}})
        # Estilo secundario: Palitos transparentes para ver densidad
        view.addStyle({'stick': {'radius': 0.1, 'opacity': 0.5}})
        
        view.zoomTo()
        view.spin(True)
        
        showmol(view, height=400, width=600)
        st.info(f"Designed Molecule: {drug.target_receptor}-Inhibitor (Stability: {drug.structure.plddt_score} pLDDT)")
    else:
        st.info("No active therapy. Inject treatment to visualize molecular design.")
