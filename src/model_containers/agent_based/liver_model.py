import random
from src.data_models.schemas import Hormokine

class LiverLobule:
    def __init__(self, fibrosis_level=0.8):
        self.fibrosis_level = fibrosis_level
        self.steps = 0
        self.hepatocyte_viability = 0.4 
        self.hsc_activation_level = 1.0 
        self.epigenetic_status = 1.0 

    def inject_treatment(self, intervention: Hormokine) -> dict:
        # 1. Targeting Logic
        affinity = intervention.predicted_affinity
        target = intervention.target.receptor

        if "TGFBR2" in target and intervention.target.action == "INHIBIT":
            reprogramming = affinity * intervention.instruction_potency
            self.hsc_activation_level -= (reprogramming * 0.5)
            self.epigenetic_status -= (reprogramming * 0.3)
            
        elif "EGFR" in target and intervention.target.action == "ACTIVATE":
            self.hepatocyte_viability += (affinity * 0.2)

        # 2. Toxicity Logic
        if intervention.immunogenicity_score > 0.4:
            self.hepatocyte_viability -= 0.1

        self._clamp_values()
        # IMPORTANT: Always update state and return status
        self.update_state() 
        return self.get_status()

    def update_state(self):
        self.steps += 1
        if self.hsc_activation_level > 0.3:
            self.fibrosis_level += 0.01
        else:
            self.fibrosis_level -= 0.005
        self._clamp_values()

    def _clamp_values(self):
        self.fibrosis_level = max(0.0, min(1.0, self.fibrosis_level))
        self.hsc_activation_level = max(0.0, min(1.0, self.hsc_activation_level))
        self.hepatocyte_viability = max(0.0, min(1.0, self.hepatocyte_viability))
        self.epigenetic_status = max(0.0, min(1.0, self.epigenetic_status))

    def get_status(self):
        return {
            "step": self.steps,
            "fibrosis_index": float(round(self.fibrosis_level, 4)),
            "hsc_activation": float(round(self.hsc_activation_level, 4)),
            "hepatocyte_viability": float(round(self.hepatocyte_viability, 4)),
            "epigenetic_status": float(round(self.epigenetic_status, 4))
        }
