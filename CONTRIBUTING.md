# Contributing to BioTwin Core 🧬

First off, thank you for considering contributing to BioTwin! It's people like you who will help us turn the vision of "programmable medicine" into a reality.

By contributing, you are helping build a framework that bridges the gap between Generative AI and Digital Twin technology.

---

## 🛠 How Can You Contribute?

### 1. 🧬 Biological Logic (New Organs & Receptors)
BioTwin is currently focused on the liver, but the architecture is organ-agnostic. You can contribute by:
* Defining new `TargetProfiles` for different diseases (e.g., Cardiac Fibrosis, Neurodegeneration).
* Researching and adding new receptors to the `liver_model.py` or creating new organ models.
* Improving the **Epigenetic Driver** logic based on real-world clinical data.

### 2. 🤖 AI & Generative Improvements
The `BioNeMoClient` currently uses a mock for simulation. We need help:
* Integrating real API calls to **NVIDIA BioNeMo**, **AlphaFold**, or **ESMFold**.
* Developing better scoring functions for `immunogenicity` and `toxicity` of protein sequences.

### 3. 💻 Software Engineering
* **Optimization:** Improving the performance of the Agent-Based Model (ABM).
* **Visualization:** Enhancing the Streamlit Dashboard or building a 3D cellular viewer using Three.js or PyVista.
* **Testing:** Writing edge-case tests for the simulation bounds in `tests/`.

---

## 🚀 Development Workflow

### 1. Setup the Environment
Follow the instructions in the [README.md](README.md) to get the Docker container running.

### 2. Coding Standards (The CI Pipeline)
We use **Flake8** for linting and **Pytest** for logic validation. Your code must pass the CI pipeline to be merged.
* Run linter: `flake8 src/`
* Run tests: `python -m pytest tests/`

### 3. Branching Strategy
* Please create a branch for your feature: `git checkout -b feature/amazing-new-receptor`.
* Open a **Pull Request (PR)** against the `main` branch.
* Describe your changes: What biological logic did you add? How does it affect the Digital Twin?

---

## 🧪 Scientific Integrity
BioTwin Core aims for rational design. When proposing changes to the simulation logic:
* Cite your sources (e.g., papers on TGF-beta signaling or HSC activation).
* Ensure that the "Programming" metaphor remains consistent: Molecules are instructions, Receptors are ports, and Cells are the hardware.



---

## 📫 Communication
* **Issues:** For bug reports or feature requests.
* **Discussions:** For "What if we simulated..." type of ideas.

Join us in building the operating system for the human body!
