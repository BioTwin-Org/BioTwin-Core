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

st.set_page_config(page_title="BioTwin: Clinical Suite", layout="wide", page_icon="🧬")

# --- GESTIÓN DE ESTADO ---
if "liver" not in st.session_state:
    st.session_state.liver = LiverModel()
    st.session_state.heart = HeartModel()
    st.session_state.pk = ADMEModel() # Nuevo Modelo PK
    st.session_state.drug = None
    st.session_state.ecg_history = [0.0] * 100
    st.session_state.trial_results = None
    st.session_state.patient_info = {"id": "Anonymous", "risk": "Unknown"}
    st.session_state.chat_history = [{"role": "assistant", "content": "System Ready. Please configure dosage."}]

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("📂 Patient Data")
    uploaded_file = st.file_uploader("Upload Genotype (.json)", type=["json"])
    if uploaded_file:
        data = json.load(uploaded_file)
        if st.session_state.patient_info["id"] != data.get("patient_id"):
            st.session_state.patient_info = {"id": data.get("patient_id"), "risk": data.get("genetic_risk_factor")}
            st.session_state.liver = LiverModel(genetic_risk=data.get("genetic_risk_factor", 1.0))
            st.success("Patient Loaded")

    st.divider()
    
    st.header("💊 Pharmacokinetics (PK)")
    # NUEVOS CONTROLES DE DOSIFICACIÓN
    dose = st.slider("Dose (mg)", 10, 200, 50, help="Amount of drug administered.")
    interval = st.slider("Frequency (hours)", 4, 24, 8, help="Time between doses.")
    
    # Actualizar configuración PK si cambia
    if st.session_state.pk.dose != dose or st.session_state.pk.interval != interval:
        st.session_state.pk = ADMEModel(dose_mg=dose, interval_hours=interval)
        st.toast("Dosing regimen updated!")

    st.divider()
    target = st.selectbox("Target", ["TGFBR2", "IL-6R"])
    mechanism = st.radio("Mechanism", ["INHIBIT", "ACTIVATE"])
    
    if st.button("♻️ RESET ALL", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.title(f"🧬 BioTwin: {st.session_state.patient_info['id']}")

# --- PESTAÑAS ---
tab_patient, tab_trial, tab_report = st.tabs(["👤 Clinical Simulation", "📊 Population Trial", "📄 Medical Report"])

# === TAB 1: SIMULACIÓN CLÍNICA ===
with tab_patient:
    c_liver, c_ctrl, c_heart = st.columns([1.2, 0.8, 1.2])
    
    # 1. HÍGADO
    with c_liver:
        st.subheader("Hepatic Function")
        fig = px.imshow(st.session_state.liver.grid, color_continuous_scale=[[0,'#2ecc71'],[1,'#e74c3c']], zmin=0, zmax=1)
        fig.update_layout(height=250, margin=dict(l=0,r=0,b=0,t=0), coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True, key=f"liv_{st.session_state.liver.step}")
        
        # Métrica de Limpieza Hepática
        clearance = st.session_state.liver.viability * 100
        st.progress(st.session_state.liver.toxicity, text=f"Toxicity: {st.session_state.liver.toxicity*100:.1f}%")
        st.caption(f"Metabolic Clearance Capacity: {clearance:.1f}%")

    # 2. CONTROLES Y PK
    with c_ctrl:
        st.subheader("Therapy Control")
        if st.button("▶ Run Step (1 Hour)", use_container_width=True):
            # A. Calcular Concentración en Sangre (PK)
            # Pasamos la salud del hígado (viabilidad) al modelo PK
            liver_health = st.session_state.liver.viability
            current_conc = st.session_state.pk.update(liver_health)
            
            # B. Calcular Efecto Real de la Droga
            # Si hay poca droga en sangre, el efecto es bajo. Si hay mucha, es alto.
            effect_factor = min(current_conc / 20.0, 1.0) # Normalizamos
            
            # C. Actualizar Hígado
            # Si hay droga, inyectamos el efecto calculado
            if st.session_state.drug:
                potency = st.session_state.drug.instruction_potency * effect_factor
                st.session_state.liver.inject_hormokine(potency, st.session_state.drug.predicted_affinity)
            
            # D. Actualizar Toxicidad Extra por Sobredosis
            overdose_tox = st.session_state.pk.get_toxicity_risk()
            st.session_state.liver.toxicity += overdose_tox
            st.session_state.liver.update_state()
            
            # E. Actualizar Corazón
            st.session_state.heart.update(st.session_state.liver.toxicity)
            st.session_state.ecg_history.append(st.session_state.heart.generate_ecg_wave())
            st.session_state.ecg_history.pop(0)
            st.rerun()

        if st.button(f"🧬 Design Drug ({mechanism})", type="primary", use_container_width=True):
            designer = HormokineDesigner()
            best = designer.optimize_design(target, mechanism, "High Risk")
            st.session_state.drug = best
            st.rerun()

        # GRÁFICA DE FARMACOCINÉTICA (PK)
        if len(st.session_state.pk.history) > 0:
            st.markdown("---")
            st.caption("📈 Plasma Concentration (mg/L)")
            pk_df = pd.DataFrame({"Hour": range(len(st.session_state.pk.history)), "Conc": st.session_state.pk.history})
            
            fig_pk = px.area(pk_df, x="Hour", y="Conc", color_discrete_sequence=["#3498db"])
            fig_pk.add_hline(y=15, line_dash="dash", line_color="red", annotation_text="Toxic Threshold")
            fig_pk.update_layout(height=150, margin=dict(l=0,r=0,b=0,t=0), yaxis_title=None, xaxis_title=None)
            st.plotly_chart(fig_pk, use_container_width=True)

    # 3. CORAZÓN
    with c_heart:
        st.subheader("Cardiac Response")
        # Animación Corazón
        bpm = st.session_state.heart.heart_rate
        sec = 60 / max(bpm, 1)
        st.markdown(f"""<div style="display:flex;justify-content:center;margin:10px;"><svg width="80" height="80" viewBox="0 0 24 24" fill="#ff0000"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"><animateTransform attributeName="transform" type="scale" values="1;1.15;1" dur="{sec}s" repeatCount="indefinite" additive="sum" calcMode="spline" keySplines="0.4 0 0.2 1;0.4 0 0.2 1"/></path></svg></div>""", unsafe_allow_html=True)
        
        fig_ecg = go.Figure()
        fig_ecg.add_trace(go.Scatter(y=st.session_state.ecg_history, mode='lines', line=dict(color='#00ff00', width=2)))
        fig_ecg.update_layout(height=100, margin=dict(l=0,r=0,b=0,t=0), paper_bgcolor='black', plot_bgcolor='black', xaxis=dict(visible=False), yaxis=dict(visible=False, range=[-2,2]))
        st.plotly_chart(fig_ecg, use_container_width=True)
        st.metric("LVEF", f"{st.session_state.heart.ejection_fraction:.1f}%")

# === TAB 2: ENSAYO (Simplificado para esta vista) ===
with tab_trial:
    st.info("Run Population Analysis to update report stats.")
    if st.button("🚀 Run Mini-Cohort (N=10)", use_container_width=True):
        res = []
        bar = st.progress(0)
        for i in range(10):
            # Simulación rápida
            h = HeartModel()
            res.append({"Outcome": "Healthy" if h.ejection_fraction > 40 else "Heart Failure"})
            bar.progress((i+1)/10)
        st.session_state.trial_results = pd.DataFrame(res)
        st.success("Cohort Data Updated")

# === TAB 3: REPORTE CLÍNICO (NUEVO) ===
with tab_report:
    st.header("📄 Clinical Report Generation")
    
    col_rep1, col_rep2 = st.columns([2, 1])
    
    with col_rep1:
        notes = st.text_area("Doctor's Notes / Observations:", "Patient shows initial response to therapy. Monitoring PK curve for accumulation risks.")
        
    with col_rep2:
        st.markdown("### Actions")
        if st.button("🖨️ Generate PDF Report", type="primary", use_container_width=True):
            # Preparar datos
            outcome = "Stable"
            if st.session_state.liver.toxicity > 0.5: outcome = "Critical (Liver)"
            if st.session_state.heart.ejection_fraction < 40: outcome = "Critical (Heart)"
            
            surv = 100
            if st.session_state.trial_results is not None:
                df = st.session_state.trial_results
                surv = (df[df["Outcome"]=="Healthy"].shape[0] / len(df)) * 100
            
            stats = {"survival": surv}
            
            # Generar PDF
            pdf_gen = ClinicalReportGenerator()
            pdf_bytes = pdf_gen.create_pdf(
                st.session_state.patient_info,
                st.session_state.drug,
                outcome,
                stats,
                notes
            )
            
            st.download_button(
                label="📥 Download PDF",
                data=pdf_bytes,
                file_name=f"Report_{st.session_state.patient_info['id']}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    # Vista previa de datos
    st.info("This report will include: Patient Genotype, PK Dosing Schedule, Current Tissue Viability, and Cohort Survival Stats.")
