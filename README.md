# 🧬 BioTwin: AI-Powered In Silico Clinical Trial Platform

**BioTwin** es una plataforma avanzada de simulación biológica y descubrimiento de fármacos diseñada para acelerar la fase preclínica y clínica mediante **Gemelos Digitales (Digital Twins)**.

La herramienta permite diseñar moléculas terapéuticas, simular su farmacocinética (PK/PD) en tiempo real y evaluar su impacto en una fisiología multi-órgano interconectada, culminando en ensayos clínicos virtuales Fase III.

---

## 🚀 Características Principales

### 1. Diseño Molecular y Generativo
* **Diseño de Fármacos 3D:** Visualización molecular interactiva utilizando `Py3Dmol`.
* **Optimización de Candidatos:** Generación automática de variantes moleculares (Agresiva, Segura, Balanceada) y comparación mediante gráficos de radar.

### 2. Fisiología Multi-Órgano (Systemic Biology)
Simulación basada en agentes (Agent-Based Modeling) de la interacción entre órganos vitales:
* **🫁 Hígado (Hepatic Model):** Simula metabolismo, toxicidad (ALT) y regeneración tisular (Fibrosis).
* **💧 Riñón (Renal Model):** Simula filtración glomerular (GFR), acumulación de creatinina y nefrotoxicidad.
* **🫀 Corazón (Cardiac Model):** Monitorización en tiempo real del ritmo cardiaco (ECG), fracción de eyección (LVEF) y riesgo de paro cardiaco.

### 3. Farmacología Avanzada
* **Farmacocinética (PK/PD):** Modelado ADME (Absorción, Distribución, Metabolismo, Excreción).
* **Polifarmacia e Interacciones:** Simulación de interacciones medicamentosas (Inhibidores/Inductores CYP450) como Omeprazol o Rifampicina.
* **Rutas de Eliminación:** Configuración de eliminación Hepática vs. Renal.

### 4. Inteligencia Artificial de Bucle Cerrado (Closed-Loop AI)
* **Auto-Titulación:** Un sistema de "Piloto Automático" que ajusta dinámicamente la dosis y frecuencia en respuesta a biomarcadores críticos para mantener la ventana terapéutica segura.

### 5. Ensayos Clínicos Virtuales
* **Stress Lab (Crash Test):** Determinación automática de la Dosis Letal (LD50) y puntos de quiebre fisiológicos.
* **Ensayo Fase III Poblacional:** Simulación estocástica de cohortes estratificadas (Sanos, Insuficiencia Renal, Daño Hepático) para validar seguridad poblacional.
* **Reportes Regulatorios:** Generación automática de dossiers PDF listos para revisión (formato FDA/EMA).

---

## 🛠️ Tecnologías Utilizadas

* **Core:** Python 3.9+
* **Frontend:** Streamlit
* **Visualización de Datos:** Plotly Express / Graph Objects
* **Visualización Molecular:** Py3Dmol / Stmol
* **Cálculo Numérico:** NumPy / Pandas
* **Reportes:** FPDF

---

## 📦 Instalación y Uso

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/biotwin.git](https://github.com/tu-usuario/biotwin.git)
    cd biotwin
    ```

2.  **Crear entorno virtual (Recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar la aplicación:**
    ```bash
    export PYTHONPATH=$PYTHONPATH:$(pwd)
    streamlit run src/dashboard/app.py
    ```

---

## 🖥️ Guía de Módulos

### Pestaña 1: Simulación Multi-Órgano (Clinical Sim)
El centro de mando principal. Aquí puedes ver el estado de los tejidos en tiempo real, diseñar la molécula base y activar el "Piloto Automático" de la IA.
* *Monitor:* Observa las curvas de concentración plasmática vs. biomarcadores (ALT, Creatinina).

### Pestaña 2: Optimización y Ensayos (Lead Optimization & Phase III)
* **Lead Optimization:** Genera 3 variantes de tu fármaco y compáralas en un torneo de eficacia vs. seguridad.
* **Phase III Trial:** Ejecuta un estudio con 40 pacientes virtuales diversos para detectar toxicidades ocultas en poblaciones vulnerables.

### Pestaña 3: Laboratorio de Estrés y Reportes
* **Stress Lab:** Somete al paciente a dosis extremas para encontrar los límites de tolerancia.
* **Regulatory Report:** Descarga el PDF con toda la evidencia generada.

---

## ⚠️ Disclaimer
*Esta herramienta es un prototipo de simulación in silico con fines educativos y de investigación. No debe utilizarse para la toma de decisiones médicas reales ni sustituye ensayos clínicos in vivo.*

---

**Desarrollado con 🧬 e 🤖 por Enrique Chacon Pinzon**
