import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import py3Dmol
from stmol import showmol
from src.model_containers.agent_based.liver_model import LiverModel
from src.model_containers.agent_based.heart_model import HeartModel # NUEVO IMPORT
from src.generative.hormokine_designer import HormokineDesigner

st.set_page_config(page_title="BioTwin: Multi-Organ System", layout="wide", page_icon="🫀")

# --- INICIALIZACIÓN DE ESTADO (AHORA CON CORAZÓN) ---
if "liver" not in st.session_state:
    st.session_state.liver = LiverModel()
    st.session_state.heart = HeartModel() # Inicializamos el corazón
    st.session_state.drug = None
    st.session_state.ecg_history = [0] * 100 # Buffer para la gráfica ECG

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🧬 System Configuration")
    target = st.selectbox("Target Receptor", ["TGFBR2", "IL-6R", "VEGFA"])
    mechanism = st.radio("Mechanism", ["INHIBIT", "ACTIVATE"])
    
    st.divider()
    
    # Monitor de Paciente
    st.subheader("Patient Vitals")
    h_rate = st.session_state.heart.heart_rate
    st.metric("Heart Rate", f"{int(h_rate)} BPM", delta=f"{int(h_rate - 75)}")
    st.metric("QT Interval", f"{int(st.session_state.heart.qt_interval)} ms")
    
    st.divider()
    if st.button("♻️ RESET SYSTEM", type="primary", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- PANEL PRINCIPAL ---
st.title("🫀 BioTwin: Cardio-Hepatic Axis")
st.caption("Systemic Simulation: Liver Toxicity induces Cardiac Stress via Inflammatory Cytokines")

# Layout: 3 Columnas (Hígado - Conexión - Corazón)
col_liver, col_mol, col_heart = st.columns([1.2, 1, 1.2])

# --- 1. HÍGADO (FUENTE DEL PROBLEMA) ---
with col_liver:
    st.subheader("1. Liver (Source)")
    fig_liver = px.imshow(st.session_state.liver.grid, 
                    color_continuous_scale=[[0, '#2ecc71'], [1, '#e74c3c']],
                    zmin=0, zmax=1)
    fig_liver.update_layout(height=350, margin=dict(l=0,r=0,b=0,t=0), coloraxis_showscale=False)
    st.plotly_chart(fig_liver, use_container_width=True, key=f"liv_{st.session_state.liver.step}")
    
    liver_status = st.session_state.liver.get_status()
    tox_val = liver_status['Toxicity']
    st.progress(tox_val, text=f"Hepatic Toxicity Output: {tox_val*100:.1f}%")

# --- 2. MOLÉCULA & CONTROLES (EL PUENTE) ---
with col_mol:
    st.subheader("2. Treatment")
    
    # Controles Centrales
    c1, c2 = st.columns(2)
    with c1:
        if st.button("▶ Run Step", use_container_width=True):
            # 1. Avanza Hígado
            st.session_state.liver.update_state()
            # 2. La toxicidad del hígado viaja al corazón
            sys_tox = st.session_state.liver.toxicity
            st.session_state.heart.update(sys_tox)
            # 3. Generar dato ECG
            new_signal = st.session_state.heart.generate_ecg_wave()
            st.session_state.ecg_history.append(new_signal)
            if len(st.session_state.ecg_history) > 100: st.session_state.ecg_history.pop(0)
            st.rerun()
            
    with c2:
        if st.button("🧬 AI Design", type="primary", use_container_width=True):
            designer = HormokineDesigner()
            best = designer.optimize_design(target, mechanism, "High Risk")
            st.session_state.drug = best
            st.session_state.liver.inject_hormokine(best.instruction_potency, best.predicted_affinity)
            st.rerun()

    # Visor Molecular Compacto
    if st.session_state.drug:
        d = st.session_state.drug
        view = py3Dmol.view(width=300, height=250)
        view.addModel(d.structure.pdb_content, 'pdb')
        view.setBackgroundColor('#0e1117')
        view.setStyle({'cartoon': {'color': 'spectrum'}})
        view.zoomTo()
        showmol(view, height=250, width=300)
        st.info(f"Drug: {d.name}")
    else:
        st.warning("No drug active")

# --- 3. CORAZÓN (ÓRGANO AFECTADO) ---
with col_heart:
    st.subheader("3. Heart (Response)")
    
    # --- VISUALIZACIÓN DE LATIDO (CSS ANIMATION) ---
    # Calculamos la velocidad de la animación basada en los BPM
    bpm = st.session_state.heart.heart_rate
    beat_duration = 60 / max(bpm, 1) # Segundos por latido
    
    st.markdown(f"""
    <div style="display: flex; justify-content: center; margin-bottom: 10px;">
        <svg width="100" height="100" viewBox="0 0 24 24" fill="red" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z">
                <animateTransform attributeName="transform" type="scale" values="1; 1.1; 1" dur="{beat_duration}s" repeatCount="indefinite" additive="sum" calcMode="spline" keySplines="0.4 0 0.2 1; 0.4 0 0.2 1"/>
            </path>
        </svg>
    </div>
    <div style="text-align: center; font-weight: bold; color: {'red' if st.session_state.heart.status != 'Normal Sinus Rhythm' else '#2ecc71'}">
        {st.session_state.heart.status}
    </div>
    """, unsafe_allow_html=True)
    
    # Monitor ECG en Tiempo Real
    ecg_fig = go.Figure()
    ecg_fig.add_trace(go.Scatter(y=st.session_state.ecg_history, mode='lines', line=dict(color='#00ff00', width=2)))
    ecg_fig.update_layout(
        height=200, 
        margin=dict(l=0,r=0,b=0,t=0), 
        paper_bgcolor='black', 
        plot_bgcolor='black',
        xaxis=dict(showgrid=False, visible=False),
        yaxis=dict(showgrid=True, gridcolor='#333333', range=[-2, 2])
    )
    st.plotly_chart(ecg_fig, use_container_width=True)
    
    # Fracción de Eyección (Gauge)
    ef = st.session_state.heart.ejection_fraction
    st.metric("Ejection Fraction (LVEF)", f"{ef:.1f}%", delta=f"{ef-60:.1f}%")

# --- GRÁFICA SISTÉMICA ---
st.divider()
st.subheader("📈 Systemic Interaction Analysis")
if len(st.session_state.liver.history) > 0:
    # Combinamos datos de ambos órganos
    hist_data = pd.DataFrame(st.session_state.liver.history)
    # Simulamos historial cardiaco alineado
    hist_data['Heart Stress'] = [x['Toxicity'] * 1.5 for x in st.session_state.liver.history]
    
    st.line_chart(hist_data.set_index("Step")[["Toxicity", "Heart Stress"]], height=250)    
