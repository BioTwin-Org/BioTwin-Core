cat <<EOF > src/dashboard/app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import py3Dmol
from stmol import showmol
from src.model_containers.agent_based.liver_model import LiverModel
from src.model_containers.agent_based.heart_model import HeartModel
from src.generative.hormokine_designer import HormokineDesigner

st.set_page_config(page_title="BioTwin: Cardio-Hepatic Axis", layout="wide", page_icon="🫀")

# INICIALIZACIÓN MULTI-ÓRGANO
if "liver" not in st.session_state:
    st.session_state.liver = LiverModel()
    st.session_state.heart = HeartModel()
    st.session_state.drug = None
    st.session_state.ecg_history = [0.0] * 100

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🫀 System Vitals")
    st.metric("Heart Rate", f"{int(st.session_state.heart.heart_rate)} BPM")
    st.metric("QT Interval", f"{int(st.session_state.heart.qt_interval)} ms")
    
    st.divider()
    target = st.selectbox("Target", ["TGFBR2", "IL-6R"])
    mechanism = st.radio("Mechanism", ["INHIBIT", "ACTIVATE"])
    
    if st.button("♻️ RESET SYSTEM", type="primary", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- PANEL PRINCIPAL ---
st.title("🫀 BioTwin: Cardio-Hepatic Simulation")
st.caption("Monitoring systemic toxicity transfer from Liver to Heart.")

# Layout de 3 columnas
c_liver, c_ctrl, c_heart = st.columns([1.2, 0.8, 1.2])

# 1. HÍGADO
with c_liver:
    st.subheader("1. Liver (Source)")
    fig = px.imshow(st.session_state.liver.grid, color_continuous_scale=[[0,'#2ecc71'],[1,'#e74c3c']], zmin=0, zmax=1)
    fig.update_layout(height=300, margin=dict(l=0,r=0,b=0,t=0), coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True, key=f"liv_{st.session_state.liver.step}")
    
    tox = st.session_state.liver.toxicity
    st.progress(tox, text=f"Systemic Toxicity: {tox*100:.1f}%")

# 2. CONTROLES Y MOLÉCULA
with c_ctrl:
    st.subheader("2. Intervention")
    if st.button("▶ Run Step", use_container_width=True):
        # Avanzar Hígado
        st.session_state.liver.update_state()
        # Avanzar Corazón (recibe toxicidad)
        st.session_state.heart.update(st.session_state.liver.toxicity)
        # Generar ECG
        new_pt = st.session_state.heart.generate_ecg_wave()
        st.session_state.ecg_history.append(new_pt)
        st.session_state.ecg_history.pop(0)
        st.rerun()

    if st.button(f"🧬 AI Design ({mechanism})", type="primary", use_container_width=True):
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
    else:
        st.info("No active drug")

# 3. CORAZÓN
with c_heart:
    st.subheader("3. Heart (Response)")
    
    # Estado Clínico
    status = st.session_state.heart.status
    color = "red" if status != "Normal Sinus Rhythm" else "green"
    st.markdown(f"Status: **:{color}[{status}]**")
    
    # Monitor ECG
    fig_ecg = go.Figure()
    fig_ecg.add_trace(go.Scatter(y=st.session_state.ecg_history, mode='lines', line=dict(color='#00ff00', width=2)))
    fig_ecg.update_layout(height=200, margin=dict(l=0,r=0,b=0,t=0), paper_bgcolor='black', plot_bgcolor='black', 
                         xaxis=dict(visible=False), yaxis=dict(range=[-2, 2], visible=False))
    st.plotly_chart(fig_ecg, use_container_width=True)
    
    ef = st.session_state.heart.ejection_fraction
    st.metric("Ejection Fraction (LVEF)", f"{ef:.1f}%")

# GRÁFICA INFERIOR
st.divider()
if len(st.session_state.liver.history) > 0:
    hist = pd.DataFrame(st.session_state.liver.history)
    hist['Cardiac Stress'] = [x['Toxicity']*1.5 for x in st.session_state.liver.history]
    st.line_chart(hist.set_index("Step")[["Toxicity", "Cardiac Stress"]], height=200)
EOF   
