
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
