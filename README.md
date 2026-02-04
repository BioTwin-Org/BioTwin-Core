# 🧬 BioTwin Core: Endogenous Reprogramming Framework

**"The human body is an analog computer that can be programmed via molecular instructions."**

BioTwin Core is an open-source framework designed to bridge Generative AI (**NVIDIA BioNeMo**) with Agent-Based Modeling (ABM) to design and simulate **Hormokines**: synthetic proteins programmed to execute specific epigenetic instructions in human tissue.

---

## 👁️ Vision & Philosophy
Traditional medicine often treats symptoms. BioTwin proposes a shift toward **Rational Biological Programming**. By using synthetic molecules as "software," we can send instructions to specific cell types to:
1.  **Silence** pathological drivers (e.g., Fibrosis in Stellate Cells).
2.  **Reactivate** regenerative pathways (e.g., Hepatocyte proliferation).
3.  **Synchronize** tissue repair using environmental sensors (Smart Release).

---

## 🏗️ System Architecture
The framework is built on a modular pipeline that ensures scientific rigor and computational efficiency.

### Core Components:
* **Generative Layer (`src/generative/`):** Interfaces with BioNeMo/ESMFold to design sequences based on target receptors (TGFBR2, IL-6R).
* **Genomic Layer (`src/data_models/genomics.py`):** Integrates AlphaGenome risk factors to stratify patient response.
* **Simulation Engine (`src/model_containers/agent_based/`):** A Multi-Agent system (Kupffer & HSC) that simulates the crosstalk in the liver lobule.
* **Validation Layer (`tests/`):** Automated CI pipeline to verify biological logic and therapeutic safety bounds.

---

## 📁 Project Structure
```text
BioTwin-Core/
├── src/
│   ├── data_models/       # Molecule & Genomic Schemas
│   ├── generative/       # AI Service (BioNeMo / ESMFold)
│   ├── model_containers/ # ABM Logic (Liver Model)
│   └── app.py            # Streamlit Interactive Dashboard
├── tests/                # Pytest Suite (Logic Validation)
├── requirements.txt      # Project Dependencies
└── README.md             # Project Documentation
