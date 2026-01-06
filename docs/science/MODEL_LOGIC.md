# Scientific Foundations of BioTwin Liver Model 🧬

This document outlines the biological rationale and mathematical assumptions behind the agent-based simulation of liver fibrosis and epigenetic reprogramming.

## 1. The Stellate Cell (HSC) Activation Pathway
Our model simulates the transition of Hepatic Stellate Cells from a quiescent (vitamin-A storing) state to an activated (myofibroblast-like) state.

* **Pathway:** TGF-β / SMAD Signaling.
* **Mechanism:** Binding of TGF-β1 to the **TGFBR2** receptor triggers SMAD2/3 phosphorylation, leading to the transcription of Type I Collagen.
* **Reference:** *Bataller, R., & Brenner, D. A. (2005). Liver fibrosis. Journal of Clinical Investigation.*

## 2. Epigenetic Reprogramming Logic
The "Instruction Potency" in our Hormokines simulates the delivery of dCas9-DNMT3A or similar epigenetic editors to the COL1A1 promoter.

* **Assumption:** Targeted DNA methylation of the promoter region leads to a stable silencing of collagen production, even in the presence of pro-inflammatory cytokines.
* **Reference:** *Zhong, J., et al. (2022). Epigenetic editing for the treatment of liver fibrosis.*

## 3. Kinetic Parameters (The "Numbers")
While currently simplified for real-time visualization, the simulation constants are being calibrated to reflect:
* **Hepatocyte Turnover:** Normal vs. Fibrotic rates.
* **Collagen Half-life:** Modeled as a decay function once HSCs are deactivated.
* **Binding Affinity ($K_d$):** Values $>0.8$ in the dashboard represent nanomolar (nM) affinity ranges typical of high-performance synthetic peptides.

## 4. Future Calibration (Roadmap)
We aim to replace the current stochastic updates with:
- **ODEs (Ordinary Differential Equations):** For precise metabolic flux analysis.
- **Single-cell RNA-seq Data:** To initialize agent states based on real patient biopsies.
