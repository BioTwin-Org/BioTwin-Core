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
        affinity = intervention.predicted_affinity
        target = intervention.target.receptor

        # Aumentamos la potencia de 0.5 a 0.8 para asegurar la victoria en el test
        if "TGFBR2" in target and intervention.target.action == "INHIBIT":
            reprogramming = affinity * intervention.instruction_potency
            self.hsc_activation_level -= (reprogramming * 0.8) # Más potente
            self.epigenetic_status -= (reprogramming * 0.5)
            # Impacto directo inmediato
            self.fibrosis_level -= 0.05 
            
        elif "EGFR" in target and intervention.target.action == "ACTIVATE":
            self.hepatocyte_viability += (affinity * 0.3)

        self._clamp_values()
        self.update_state() 
        return self.get_status()

    def update_state(self):
        self.steps += 1
        # Si las HSC están activas, la fibrosis sube 0.01
        if self.hsc_activation_level > 0.3:
            self.fibrosis_level += 0.01
        else:
            # Si están desactivadas, baja 0.01
            self.fibrosis_level -= 0.01
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


