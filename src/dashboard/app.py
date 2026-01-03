import streamlit as st
import pandas as pd
import time
import sys
import os

# Asegurar que Streamlit encuentre los módulos del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.generative.bionemo_client import BioNeMoClient
from src.model_containers.agent_based.liver_model import LiverLobule
from src.data_models.schemas import Hormokine, TargetProfile

# Configuración de la página
st.set_page_config(
    page_title="BioTwin Core | Dashboard",
    page_icon="🧬",
    layout="wide"
)

# Título y Descripción
st.title("🧬 BioTwin Core: Reprogramación Endocrina")
st.markdown("""
**Panel de Control de Gemelo Digital.** Diseñe una Hormokina, inyéctela en el tejido virtual y observe la respuesta fisiológica en tiempo real.
*Basado en la arquitectura: El cuerpo como computadora analógica programable.*
""")

# --- BARRA LATERAL: DISEÑO DE HORMOKINA (IA) ---
st.sidebar.header("1. Diseño Generativo (BioNeMo)")

target_receptor = st.sidebar.selectbox(
    "Receptor Objetivo",
    ["TGFBR2 (Fibrosis Driver)", "EGFR (Regeneration)", "DOPAMINE_R (Off-target)"]
)

action_type = st.sidebar.selectbox(
    "Acción Farmacológica",
    ["INHIBIT", "ACTIVATE"]
)

st.sidebar.markdown("---")
st.sidebar.info("El modelo de IA generará una secuencia de proteína optimizada para estos parámetros.")

if st.sidebar.button("Generar Candidato"):
    with st.spinner("Conectando con BioNeMo Model (Sim)..."):
        # Instanciar cliente IA
        ai_client = BioNeMoClient()
        candidate = ai_client.generate_hormokine(target_receptor, action_type)
        
        # Guardar en sesión para usarlo después
        st.session_state['candidate'] = candidate
        st.success("¡Hormokina Diseñada!")

# Mostrar candidato si existe
if 'candidate' in st.session_state:
    c = st.session_state['candidate']
    st.sidebar.markdown("### Candidato Actual")
    st.sidebar.code(f"ID: {c.intervention_id}\nSeq: {c.sequence[:10]}...")
    st.sidebar.metric("Afinidad Predicha", f"{c.predicted_affinity:.2f}")

# --- PANEL PRINCIPAL: SIMULACIÓN (GEMELO DIGITAL) ---
col1, col2 = st.columns([2, 1])

with col1:
    st.header("2. Simulación Fisiológica (LiverVerse)")
    
    # Botón para iniciar simulación
    start_sim = st.button("💉 Inyectar Tratamiento e Iniciar Simulación", type="primary")
    
    # Contenedor para el gráfico en tiempo real
    chart_placeholder = st.empty()
    stats_placeholder = st.empty()

    if start_sim and 'candidate' in st.session_state:
        # Inicializar Gemelo con Fibrosis Alta
        liver = LiverLobule(fibrosis_level=0.90)
        candidate = st.session_state['candidate']
        
        # Historial para graficar
        history = []
        
        # Bucle de simulación temporal (simulamos 20 pasos de tiempo)
        progress_bar = st.progress(0)
        
        for step in range(20):
            # En el paso 5 inyectamos el tratamiento
            if step == 5:
                st.toast(f"Inyectando {candidate.intervention_id}...", icon="💉")
                liver.inject_treatment(candidate)
            else:
                liver.update_state() # Evolución natural
            
            # Recopilar datos
            status = liver.get_status()
            history.append(status)
            
            # Actualizar gráfico dinámico
            df = pd.DataFrame(history)
            
            # Crear gráfico de líneas
            chart_placeholder.line_chart(
                df[['fibrosis_index', 'hepatocyte_viability']],
                height=350
            )
            
            # Actualizar métricas
            with stats_placeholder.container():
                m1, m2, m3 = st.columns(3)
                m1.metric("Paso Temporal", f"{status['step']}")
                m2.metric("Índice Fibrosis", f"{status['fibrosis_index']:.2f}", delta_color="inverse")
                m3.metric("Viabilidad Celular", f"{status['hepatocyte_viability']:.2f}")

            time.sleep(0.1) # Velocidad de animación
            progress_bar.progress((step + 1) / 20)
            
        st.success("Simulación Finalizada")

    elif start_sim and 'candidate' not in st.session_state:
        st.error("Primero genere una Hormokina en el panel lateral.")

with col2:
    st.header("Diagnóstico")
    st.info("""
    **Interpretación:**
    * **Línea Azul (Fibrosis):** Debe bajar tras la inyección (Paso 5) si el tratamiento es correcto.
    * **Línea Roja (Viabilidad):** Debe subir a medida que el tejido sana.
    """)
    with st.expander("Ver Logs del Sistema"):
        st.write("Esperando ejecución...")
