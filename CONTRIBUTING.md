# Contributing to BioTwin-Core

Thank you for your interest in contributing to the **BioTwin-Core** project! We are building the first open-source Digital Twin engine for endogenous regenerative medicine.

To ensure a smooth collaboration, please review the following guidelines.

## 🤝 How to Contribute

We welcome contributions from:
* **Biologists:** Validating mechanistic rules and providing data parameters.
* **AI Engineers:** Improving BioNeMo integration and generative models.
* **Developers:** Optimizing the simulation engine and Docker architecture.

### 1. The Workflow
We follow a standard **Fork & Pull Request** workflow:

1.  **Fork** the repository on GitHub.
2.  **Clone** your fork locally:
    ```bash
    git clone [https://github.com/BioTwin-Org/BioTwin-Core.git](https://github.com/BioTwin-Org/BioTwin-Core.git)
    ```
3.  **Create a Branch** for your feature or fix:
    ```bash
    git checkout -b feature/amazing-new-cell-type
    ```
4.  **Make your changes**. Ensure you follow the coding standards below.
5.  **Test your changes**:
    ```bash
    # Run the test suite
    pytest
    ```
6.  **Commit and Push**:
    ```bash
    git commit -m "feat: add stellate cell activation logic"
    git push origin feature/amazing-new-cell-type
    ```
7.  **Open a Pull Request (PR)** against the `main` branch of the original repository.

---

## 💻 Development Environment

### Requirements
* **Docker Desktop** (essential for running the full stack).
* **Python 3.9+** (if running locally without Docker).
* **NVIDIA GPU** (Optional, but recommended for BioNeMo training tasks).

### Setting up (Windows/Linux/Mac)
We provide a `docker-compose` setup to guarantee reproducibility.

1.  Copy the example env file:
    * *Windows (PowerShell):* `Copy-Item .env.example .env`
    * *Linux/Mac:* `cp .env.example .env`
2.  Build the stack:
    ```bash
    docker-compose up --build
    ```

---

## 🎨 Coding Standards

* **Language:** Python 3.9+.
* **Style:** We follow [PEP 8](https://peps.python.org/pep-0008/).
* **Docstrings:** All classes and functions must have docstrings explaining inputs, outputs, and biological context.

```python
def secrete_cytokine(concentration: float):
    """
    Simulates the release of inflammatory cytokines.
    
    Args:
        concentration (float): The molar concentration (nM).
    """
    pass
