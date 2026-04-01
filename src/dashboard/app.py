import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import py3Dmol
import json
from stmol import showmol
from src.model_containers.agent_based.liver_model import LiverModel
from src.model_containers.agent_based.heart_model import HeartModel
from src.model_containers.pharmacokinetics import ADMEModel
from src.generative.hormokine_designer import HormokineDesigner
from src.ai.doctor_service import DoctorService
from src.utils.report_generator import ClinicalReportGenerator

st.set_page_config(page_title="BioTwin 2.3: Cardiac Monitor", layout="wide", page_icon="🫀")

# --- ESTADO ---
if "liver" not in st.session_state:
    st.session_state.liver = LiverModel()
    st.session_state.heart = HeartModel()
    st.session_state.pk = ADMEModel()
    st.session_state.drug = None
    st.session_state.ecg_history = [0.0] * 100
    # NUEVO: Historial de Frecuencia Cardiaca
    st.session_state.bpm_history = [] 
    st.session_state.trial_results = None
    st.session_state.patient_info = {"id": "Anonymous", "risk": "Unknown"}

# --- SIDEBAR ---
with st.sidebar:
    st.header("📂 BioTwin Config")
    uploaded = st.file_uploader("Upload Genotype (.json)", type=["json"])
    if uploaded:
        data = json.load(uploaded)
        if st.session_state.patient_info["id"] != data.get("patient_id"):
            st.session_state.patient_info = {"id": data.get("patient_id"), "risk": data.get("genetic_risk_factor")}
            st.session_state.liver = LiverModel(genetic_risk=data.get("genetic_risk_factor", 1.0))
            st.success("Patient Data Loaded")

    st.divider()
    dose = st.slider("Dose (mg)", 10, 200, 50)
    freq = st.slider("Frequency (hrs)", 4, 24, 8)
    if st.session_state.pk.dose != dose or st.session_state.pk.interval != freq:
        st.session_state.pk = ADMEModel(dose_mg=dose, interval_hours=freq)
    
    st.divider()
    target = st.selectbox("Target", ["TGFBR2", "IL-6R"])
    mech = st.radio("Mechanism", ["INHIBIT", "ACTIVATE"])
    
    if st.button("♻️ RESET SYSTEM", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.title(f"🧬 BioTwin: {st.session_state.patient_info['id']}")

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["👤 Clinical Sim", "📊 Cohort Analysis", "📄 Medical Report"])

with tab1:
    c1, c2, c3 = st.columns([1.2, 0.8, 1.2])
    
    # COLUMNA 1: HÍGADO
    with c1: 
        st.subheader("Hepatic Tissue")
        fig = px.imshow(st.session_state.liver.grid, color_continuous_scale=[[0,'#2ecc71'],[1,'#e74c3c']], zmin=0, zmax=1)
        fig.update_layout(height=250, margin=dict(l=0,r=0,b=0,t=0), coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True, key=f"map_{st.session_state.liver.step}")
        st.progress(st.session_state.liver.toxicity, text=f"Toxicity: {st.session_state.liver.toxicity*100:.1f}%")

    # COLUMNA 2: INTERVENCIÓN
    with c2: 
        st.subheader("Intervention")
        
        if st.button("🧬 Design Drug", type="primary", use_container_width=True):
            des = HormokineDesigner()
            risk = "High Risk" if str(st.session_state.patient_info["risk"]) > "1.5" else "Standard"
            best = des.optimize_design(target, mech, risk)
            st.session_state.drug = best
            st.rerun()

        if st.session_state.drug:
            d = st.session_state.drug
            view = py3Dmol.view(width=300, height=250)
            view.addModel(d.structure.pdb_content, 'pdb')
            view.setBackgroundColor('#0e1117')
            view.setStyle({'chain': 'A'}, {'cartoon': {'color': 'spectrum', 'thickness': 0.8}})
            view.setStyle({'chain': 'B'}, {'stick': {'colorscheme': 'whiteCarbon', 'radius': 0.3}})
            view.zoomTo()
            view.spin(True)
            showmol(view, height=250, width=300)
            st.caption(f"Candidate: {d.name}")
        
        st.divider()
        if st.button("▶ Run 1 Hour", use_container_width=True):
            # PK Logic
            conc = st.session_state.pk.update(st.session_state.liver.viability)
            effect = min(conc / 20.0, 1.0)
            if st.session_state.drug:
                potency = st.session_state.drug.instruction_potency * effect
                st.session_state.liver.inject_hormokine(potency, st.session_state.drug.predicted_affinity)
            overdose = st.session_state.pk.get_toxicity_risk()
            st.session_state.liver.toxicity += overdose
            
            # Update Organs
            st.session_state.liver.update_state()
            st.session_state.heart.update(st.session_state.liver.toxicity)
            
            # Guardar datos históricos
            st.session_state.ecg_history.append(st.session_state.heart.generate_ecg_wave())
            st.session_state.ecg_history.pop(0)
            st.session_state.bpm_history.append(st.session_state.heart.heart_rate) # Guardamos BPM
            
            st.rerun()

        if len(st.session_state.pk.history) > 0:
            st.markdown("---")
            df_pk = pd.DataFrame({"Time": range(len(st.session_state.pk.history)), "Conc": st.session_state.pk.history})
            fig_pk = px.area(df_pk, x="Time", y="Conc", color_discrete_sequence=["#3498db"])
            fig_pk.add_hline(y=15, line_dash="dash", line_color="red")
            fig_pk.update_layout(height=100, margin=dict(l=0,r=0,b=0,t=0), xaxis_title=None, yaxis_title=None)
            st.plotly_chart(fig_pk, use_container_width=True)

    # COLUMNA 3: MONITOR CARDIACO (MEJORADO)
    with c3: 
        st.subheader("Cardiac Monitor")
        current_bpm = st.session_state.heart.heart_rate
        
        # 1. ANIMACIÓN CORAZÓN + DATO DECIMAL
        c_anim, c_val = st.columns([1, 1.5])
        with c_anim:
             st.markdown(f"""<div style="display:flex;justify-content:center;margin-top:10px;"><svg width="50" height="50" viewBox="0 0 24 24" fill="#ff0000"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"><animateTransform attributeName="transform" type="scale" values="1;1.2;1" dur="{60/max(current_bpm,1)}s" repeatCount="indefinite" additive="sum" calcMode="spline" keySplines="0.4 0 0.2 1;0.4 0 0.2 1"/></path></svg></div>""", unsafe_allow_html=True)
        with c_val:
            # Dato con decimales y color condicional
            color_bpm = "normal"
            if current_bpm > 100: color_bpm = "off" # Rojo en Streamlit metric
            st.metric("Heart Rate", f"{current_bpm:.1f} BPM", delta=f"{current_bpm - 75:.1f}", delta_color=color_bpm)

        # 2. MONITOR ECG (Instantáneo)
        st.caption("Real-time ECG Lead II")
        fig_ecg = go.Figure()
        fig_ecg.add_trace(go.Scatter(y=st.session_state.ecg_history, line=dict(color='#00ff00', width=2)))
        fig_ecg.update_layout(height=80, margin=dict(l=0,r=0,b=0,t=0), paper_bgcolor='black', plot_bgcolor='black', xaxis=dict(visible=False), yaxis=dict(visible=False, range=[-2,2]))
        st.plotly_chart(fig_ecg, use_container_width=True)

        # 3. GRÁFICA DE TENDENCIA BPM (Histórico) - NUEVO
        if len(st.session_state.bpm_history) > 0:
            st.divider()
            st.caption("📈 Heart Rate Trend (BPM)")
            df_bpm = pd.DataFrame({"Hour": range(len(st.session_state.bpm_history)), "
