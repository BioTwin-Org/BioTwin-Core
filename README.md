# 🧬 BioTwin Core: Endogenous Reprogramming Framework

**"The human body is an analog computer that can be programmed via molecular instructions."**

BioTwin Core is an open-source framework designed to bridge Generative AI (NVIDIA BioNeMo) with Agent-Based Modeling (ABM) to design and simulate **Hormokines**: synthetic proteins programmed to execute specific epigenetic instructions in human tissue.

---

## 👁️ Vision & Philosophy
Traditional medicine often treats symptoms. BioTwin proposes a shift toward **Rational Biological Programming**. By using synthetic molecules as "software," we can send instructions to specific cell types to:
1.  **Silence** pathological drivers (e.g., Fibrosis in Stellate Cells).
2.  **Reactivate** regenerative pathways (e.g., Hepatocyte proliferation).
3.  **Synchronize** tissue repair using environmental sensors (Smart Release).

---

## 🏗️ System Architecture
The framework is built on a modular pipeline that ensures scientific rigor and computational efficiency.

### 🔬 Scientific Validation
The biological logic of this simulation is documented in our [Science Folder](./docs/science/MODEL_LOGIC.md). We base our Agent-Based Model on established TGF-β/SMAD signaling pathways and epigenetic silencing research.

### Core Components:
* **Generative Layer:** Interfaces with BioNeMo to design sequences based on target receptors (TGFBR2, EGFR).
* **Protocol Layer (`schemas.py`):** Standardizes the "Hormokine" object, including its Instruction and Addressing domains.
* **Simulation Engine (`liver_model.py`):** A Multi-Agent system that simulates the crosstalk between Hepatocytes and Hepatic Stellate Cells (HSCs).
* **Validation Layer (`pytest`):** Automated CI pipeline to verify biological logic and safety bounds.

---

## 📁 Project Structure
```text
BioTwin-Core/
├── src/
│   ├── data_models/       # JSON Schemas & Data Classes
│   ├── generative/       # AI Clients (BioNeMo / Mock)
│   ├── model_containers/ # Digital Twin logic (Liver Lobule)
│   └── dashboard/        # Streamlit UI
├── tests/                # Automated logic validation
├── docker-compose.yml    # Containerized environment
└── README.md             # Project documentation
🚀 Getting Started (Example Usage)
1. Run the Environment
Ensure you have Docker installed, then run:

Bash

docker-compose up --build
Access the dashboard at http://localhost:8501.

2. Design a Treatment
In the sidebar, select a target. For example, to treat Liver Fibrosis:

Target: TGFBR2 (Transforming Growth Factor Beta Receptor 2).

Action: INHIBIT.

AI Engine: Generates a sequence with optimized Binding Affinity and Safety Score.

3. Run the Digital Twin
Inject the Hormokine and observe the real-time graph. You will see:

HSC Activation drop (Epigenetic silencing).

Fibrosis Index decrease (Tissue repair).

Cell Health stabilize or increase (Regeneration).
## 📊 Data Transparency & Validation

BioTwin Core promotes reproducible science. Every simulation generates a clinical-grade CSV report designed for downstream statistical analysis in R, Python (Pandas), or Excel.

### CSV Schema Definitions
When you download a report (e.g., `BioTwin_Report_HK-XXXX.csv`), you will find the following parameters:

| Column | Unit | Description |
| :--- | :--- | :--- |
| `step` | Time-step | Discrete simulation intervals (1 step ≈ arbitrary biological time unit). |
| `fibrosis_index` | 0.0 - 1.0 | Quantitative measure of Extracellular Matrix (ECM) accumulation. |
| `hsc_activation` | 0.0 - 1.0 | Phenotypic state of Hepatic Stellate Cells (0=Quiescent, 1=Fully Activated/Myofibroblast). |
| `hepatocyte_viability` | 0.0 - 1.0 | Ratio of functional liver cells vs. necrotic/apoptotic tissue. |

### How to Validate the Model
Researchers can verify the "Hormokine" efficiency by calculating the **Inhibition Slope**:
1. Identify the injection step (default: Step 5).
2. Measure the delta ($\Delta$) of `hsc_activation` over the subsequent 10 steps.
3. Compare the recovery rate of `hepatocyte_viability` against the `fibrosis_index` decay.

> **Note:** Our current kinetic model assumes a non-linear relationship where HSC silencing precedes collagen degradation, reflecting the real-world latency of tissue remodeling.
🤝 Contributing
We are building the future of programmable medicine. We welcome:

Bioinformaticians: To refine the protein-receptor affinity models.

Software Engineers: To scale the simulation to 3D voxel-based models.

Medical Researchers: To define new TargetProfiles for different organs.

Check our CONTRIBUTING.md (coming soon) for more details.

Disclaimer: BioTwin Core is a research-oriented simulation framework. It is not intended for clinical use or direct medical application.


