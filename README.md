# 🧬 BioTwin Core: AI-Powered Digital Twin Platform

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b)
![BioTwin](https://img.shields.io/badge/BioTwin-AlphaGenome-green)
![Status](https://img.shields.io/badge/Status-Operational-brightgreen)

> **Precision Medicine Revolution:** Simulación de tejidos, diseño de fármacos con IA generativa y ensayos clínicos virtuales en una sola plataforma.

---

## 🚀 Descripción General

**BioTwin Core** es una plataforma avanzada de bioingeniería computacional que crea **Gemelos Digitales** de pacientes para probar terapias personalizadas antes de aplicarlas en el mundo real.

El sistema integra biología de sistemas, modelado basado en agentes y **Genómica Computacional (AlphaGenome)** para simular cómo un fármaco específico afecta no solo al órgano objetivo (Hígado), sino también al sistema sistémico (Corazón).

---

## 🧠 Powered by AlphaGenome™

El núcleo de la personalización de BioTwin reside en su módulo **AlphaGenome Service**.

### ¿Qué es AlphaGenome?
Es el motor de ingestión de datos genómicos que transforma datos crudos de pacientes en parámetros de simulación vivos.

* **Entrada:** Archivos `.json` con perfil genético, biomarcadores y factores de riesgo.
* **Procesamiento:**
    * Decodifica el **Factor de Riesgo Genético** para ajustar la sensibilidad del tejido.
    * Configura el **Nivel de Fibrosis Basal** del hígado virtual.
    * Calibra la **Fisiología Cardiaca** (QTc basal, Frecuencia Cardiaca).
* **Resultado:** Un Gemelo Digital que no es un modelo genérico, sino una réplica computacional de un paciente específico (ej. *PT-2024-X99*).

---

## 🌟 Características Principales

### 1. 🔬 Análisis Espacial de Tejidos
Simulación visual en tiempo real de la interacción fármaco-tejido.
* **Liver Model:** Grilla de 50x50 agentes que simula células sanas, fibróticas e inflamadas.
* **Dinámica:** Observa cómo la toxicidad se propaga o cómo el tejido se regenera.

### 2. 🫀 Eje Cardio-Hepático (Multi-Organ Simulation)
Simulación sistémica conectada.
* **Monitor ECG en Tiempo Real:** Visualización de latidos y ondas QRS.
* **Toxicidad Sistémica:** El fallo hepático libera citocinas que estresan al corazón, afectando la Fracción de Eyección (LVEF).

### 3. 💊 Diseño de Hormocinas con IA
Generador de moléculas terapéuticas.
* Diseña proteínas 3D (archivos `.pdb`) optimizadas para receptores específicos (TGFBR2, IL-6R).
* Visualizador molecular interactivo (Stick/Cartoon/Spectrum).

### 4. 📊 Ensayos Clínicos Virtuales (Fase II)
* Simulación masiva de cohortes (N=50 pacientes).
* Analítica de patrones: Descubre correlaciones entre riesgo genético y fallo terapéutico.
* Gráficos de dispersión y distribución de toxicidad.

### 5. 💬 Doctor AI Assistant
* Chatbot médico integrado capaz de leer el estado de la simulación y resumir resultados de ensayos clínicos en lenguaje natural.

---

## 🛠️ Instalación y Uso

### Prerrequisitos
* Python 3.8+
* Entorno virtual recomendado.

### 1. Clonar e Instalar
```bash
git clone [https://github.com/tu-usuario/BioTwin-Core.git](https://github.com/tu-usuario/BioTwin-Core.git)
cd BioTwin-Core
pip install -r requirements.txt
