# BioTwin Core v2.0 🧬

**AI-Driven Endogenous Reprogramming Platform for Liver Fibrosis**

![License](https://img.shields.io/badge/license-MIT-blue)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![AlphaGenome](https://img.shields.io/badge/Integration-AlphaGenome-purple)

## 🚀 Overview
BioTwin Core is a "Bio-Operating System" that creates Digital Twins of liver tissue. It integrates **NVIDIA BioNeMo** (Generative Protein Design) and **Google DeepMind's AlphaGenome** (Genomic Stratification) to simulate and reverse fibrosis via synthetic Hormokines.

## 🏗 Architecture
* **Agent-Based Model (ABM):** Simulates interaction between Hepatocytes, Kupffer Cells (M1/M2), and Stellate Cells (HSC).
* **Generative AI:** Uses ESMFold to predict 3D structures of therapeutic ligands.
* **Genomic Layer:** Stratifies patient risk using real-world SNP data (e.g., *rs1800795*).

## 💻 Tech Stack
* **Core:** Python 3.9
* **Interface:** Streamlit + Py3Dmol (WebGL)
* **AI Services:** BioNeMo API (Mock/Production)
* **Testing:** Pytest & Flake8

## 🛠 Installation
```bash
git clone [https://github.com/YourUser/BioTwin-Core.git](https://github.com/YourUser/BioTwin-Core.git)
pip install -r requirements.txt
streamlit run app.py
