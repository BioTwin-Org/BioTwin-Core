import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import py3Dmol
from stmol import showmol
from src.model_containers.agent_based.liver_model import LiverModel
from src.model_containers.agent_based.heart_model import HeartModel
from src.generative.hormokine_designer import HormokineDesigner
from src.ai.doctor_service import DoctorService  # NUEVO IMPORT

st.set_page_config(page_title="BioTwin: Ultimate Platform", layout="wide", page_icon="🧬")

# --- GESTIÓN DE ESTADO ---
if "liver" not in st.session_state:
    st.session_state.liver = LiverModel()
    st.session_state.heart = HeartModel()
    st.session_state.drug = None
    st.session_state.ecg_history = [0.0] * 100
    st.session_state.trial_results = None
    # Historial del Chat
    st.session_state.chat_history = [{"role": "assistant", "content": "Hello! I am BioTwin AI. Ask me about the patient vitals or trial results."}]

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Configuration")
    target = st.selectbox("Drug Target", ["TGFBR2", "IL-6R"])
    mechanism = st.radio("Mechanism", ["INHIBIT", "ACTIVATE"])
    st.divider()
    if st.button("♻️ RESET ALL", type="primary", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.title("🧬 BioTwin: Advanced Therapeutics Platform")

# --- TRES PESTAÑAS ---
tab_patient, tab_trial, tab_chat = st.tabs(["👤 Single Patient", "📊 Clinical Trial", "💬 Doctor AI"])

# === TAB 1: PACIENTE ===
with tab_patient:
    c_liver, c_ctrl, c_heart = st.columns([1.2, 0.8, 1.2])
    with c_liver:
        st.subheader("Hepatic Status")
        fig = px.imshow(st.session_state.liver.grid, color_continuous_scale=[[0,'#2ecc71'],[1,'#e74c3c']], zmin=0, zmax=1)
        fig.update_layout(height=300, margin=dict(l=0,r=0,b=0,t=0), coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True, key=f"liv_{st.session_state.liver.step}")
        st.progress(st.session_state.liver.toxicity, text=f"Toxicity: {st.session_state.liver.toxicity*100:.1f}%")

    with c_ctrl:
        st.subheader("Controls")
        if st.button("▶ Run Step", use_container_width=True):
            st.session_state.liver.update_state()
            st.session_state.heart.update(st.session_state.liver.toxicity)
            new_pt = st.session_state.heart.generate_ecg_wave()
            st.session_state.ecg_history.append(new_pt)
            st.session_state.ecg_history.pop(0)
            st.rerun()

        if st.button(f"🧬 Design Drug ({mechanism})", type="primary", use_container_width=True):
            designer = HormokineDesigner()
            best = designer.optimize_design(target, mechanism, "High Risk")
            st.session_state.drug = best
            st.session_state.liver.inject_hormokine(best.instruction_potency, best.predicted_affinity)
            st.rerun()

        if st.session_state.drug:
            d = st.session_state.drug
            view = py3Dmol.view(width=250, height=200)
            view.addModel(d.structure.pdb_content, 'pdb')
            view.setBackgroundColor('#0e1117')
            view.setStyle({'cartoon': {'color': 'spectrum'}})
            view.zoomTo()
            showmol(view, height=200, width=250)

    with c_heart:
        st.subheader("Cardiac Response")
        bpm_val = st.session_state.heart.heart_rate
        sec_per_beat = 60 / max(bpm_val, 1)
        st.markdown(f"""
        <div style="display: flex; justify-content: center; margin: 10px;">
            <svg width="100" height="100" viewBox="0 0 24 24" fill="#ff0000">
                <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z">
                    <animateTransform attributeName="transform" type="scale" values="1; 1.15; 1" dur="{sec_per_beat}s" repeatCount="indefinite" additive="sum" calcMode="spline" keySplines="0.4 0 0.2 1; 0.4 0 0.2 1" />
                </path>
            </svg>
        </div>
        """, unsafe_allow_html=True)
        fig_ecg = go.Figure()
        fig_ecg.add_trace(go.Scatter(y=st.session_state.ecg_history, mode='lines', line=dict(color='#00ff00', width=2)))
        fig_ecg.update_layout(height=120, margin=dict(l=0,r=0,b=0,t=0), paper_bgcolor='black', plot_bgcolor='black', 
                            xaxis=dict(visible=False), yaxis=dict(range=[-2, 2], visible=False))
        st.plotly_chart(fig_ecg, use_container_width=True)

# === TAB 2: ENSAYO CLÍNICO ===
with tab_trial:
    st.header("📊 Virtual Clinical Trial (Phase II)")
    col_trial_ctrl, col_trial_res = st.columns([1, 2])
    with col_trial_ctrl:
        if st.button("🚀 LAUNCH TRIAL", type="primary", use_container_width=True):
            if not st.session_state.drug:
                st.error("Design a drug first!")
            else:
                results = []
                bar = st.progress(0, text="Simulating...")
                for i in range(50):
                    liv = LiverModel(genetic_risk=np.random.uniform(0.8, 2.5))
                    hrt = HeartModel()
                    drug = st.session_state.drug
                    liv.inject_hormokine(drug.instruction_potency, drug.predicted_affinity)
                    for _ in range(15):
                        liv.update_state()
                        hrt.update(liv.toxicity)
                    outcome = "Healthy"
                    if hrt.ejection_fraction < 40: outcome = "Heart Failure"
                    if liv.viability < 0.3: outcome = "Liver Failure"
                    results.append({"Patient ID": f"PT-{i:03d}", "Genetic Risk": liv.genetic_risk, "Outcome": outcome})
                    bar.progress((i+1)/50)
                st.session_state.trial_results = pd.DataFrame(results)
                bar.empty()
                st.success("Trial Completed!")

    with col_trial_res:
        if st.session_state.trial_results is not None:
            df = st.session_state.trial_results
            alive = df[df["Outcome"] == "Healthy"].shape[0]
            st.metric("Survival Rate", f"{(alive/50)*100:.1f}%")
            st.dataframe(df, height=300)

# === TAB 3: DOCTOR AI (NUEVO) ===
with tab_chat:
    st.header("💬 AI Medical Consultant")
    st.caption("Ask about patient status, trial efficacy, or drug details.")
    
    # Mostrar historial
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input del usuario
    if prompt := st.chat_input("Ask Doctor AI (e.g., 'How is the patient?', 'Summarize trial results')"):
        # 1. Mostrar pregunta usuario
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 2. Generar respuesta
        doctor = DoctorService()
        response = doctor.consult(prompt, st.session_state)
        
        # 3. Mostrar respuesta AI
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
