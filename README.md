# 🧬 BioTwin Core: Endogenous Reprogramming Framework

**"The human body is an analog computer that can be programmed via molecular instructions."**

BioTwin Core is an open-source framework designed to bridge Generative AI (NVIDIA BioNeMo) with Agent-Based Modeling (ABM) to design and simulate **Hormokines**: synthetic proteins programmed to execute specific epigenetic instructions in human tissue.

---

## 👁️ Vision & Philosophy
Traditional medicine often treats symptoms. BioTwin proposes a shift toward **Rational Biological Programming**. By using synthetic molecules as "software," we can send instructions to specific cell types to silence pathological drivers and reactivate regenerative pathways.

---

## 🚀 Simulation Showcase: Reversing Liver Fibrosis

Our latest simulation demonstrates the successful reprogramming of the liver microenvironment using the AI-designed candidate **HK-5CE55878**.

### 1. Real-Time Physiological Telemetry
As shown in the dashboard, we achieved a **total reversal of fibrosis (1.00 -> 0.00)** by precisely inhibiting the activation of Hepatic Stellate Cells (HSCs).

![BioTwin Simulation Overview](BioTwinCore_Sim2_pg1.png)

* **HSC Inhibition:** Activation levels dropped from **0.98 to 0.04** in 40 steps.
* **Fibrosis Index:** Total matrix degradation achieved, reaching **0.00** at the end of the cycle.
* **Cell Health:** Hepatocyte viability stabilized at **0.40** during the transition.

### 2. Hormokine Identity Card (Molecular Design)
Every candidate is generated with a unique identity card that includes its sequence, predicted binding affinity, and safety profile.

![Hormokine Identity Card](BioTwinCore_Sim2_pg2.png)

* **Target:** TGFBR2 (Stellate Cells).
* **Binding Affinity:** 89.97% (High Potency).
* **Safety Profile:** Verified for Digital Twin Simulation.

---

## 🏗️ System Architecture
The framework is built on a modular pipeline:

* **Generative Layer:** Designs sequences based on target receptors (TGFBR2, EGFR).
* **Protocol Layer:** Standardizes the "Hormokine" object (Instruction + Addressing domains).
* **Simulation Engine:** A Multi-Agent system that simulates crosstalk between Hepatocytes and HSCs.
* **Validation Layer:** Automated logic validation and safety bounds.

---

## 📁 Project Structure
```text
BioTwin-Core/
├── src/
│   ├── data_models/       # JSON Schemas & Data Classes
│   ├── generative/       # AI Clients (BioNeMo / Mock)
│   ├── model_containers/ # Digital Twin logic (Liver Lobule)
│   └── dashboard/        # Streamlit UI
├── docs/
│   └── science/          # Biological rationale & references
├── tests/                # Automated logic validation
└── docker-compose.yml    # Containerized environment

🧪 Scientific Foundation
The biological logic is grounded in established TGF-β/SMAD signaling pathways. For a deep dive into the mathematical assumptions and papers used to build this model, please visit our Science Documentation.
🤝 Contributing
We are building the operating system for the human body. We welcome:

Bioinformaticians: To refine protein-receptor affinity models.

Software Engineers: To scale simulations to 3D voxel-based models.

Medical Researchers: To define new TargetProfiles for different organs.

Check our CONTRIBUTING.md for more details.

Disclaimer: BioTwin Core is a research-oriented simulation framework. It is not intended for clinical use or direct medical application.
