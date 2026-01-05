import random
from src.data_models.schemas import Hormokine

class LiverLobule:
    """
    Multi-Agent Simulation: Interaction between Hepatocytes and Stellate Cells (HSCs).
    """
    def __init__(self, fibrosis_level=0.8):
        self.fibrosis_level = fibrosis_level
        self.steps = 0
        
        # AGENTE 1: Hepatocitos (Salud funcional)
        self.hepatocyte_viability = 0.4 
        
        # AGENTE 2: Células Estrelladas (HSCs - Activación pro-fibrosis)
        # 1.0 = Activadas (Produciendo colágeno), 0.0 = Inactivas/Quiescentes
        self.hsc_activation_level = 1.0 
        
        # Estado Epigenético (Driver central)
        self.epigenetic_status = 1.0 

    def inject_treatment(self, intervention: Hormokine) -> dict:
        print(f"💉 [BioTwin] Injecting {intervention.intervention_id}...")
        
        # Sensor de inflamación (solo actúa si hay daño)
        if self.fibrosis_level < 0.2:
            return self.get_status()

        affinity = intervention.predicted_affinity
        target = intervention.target.receptor

        # LÓGICA DE PROGRAMACIÓN CELULAR ESPECÍFICA
        if "TGFBR2" in target and intervention.target.action == "INHIBIT":
            # Objetivo: Desactivar las HSCs para detener la producción de colágeno
            reprogramming = affinity * intervention.instruction_potency
            self.hsc_activation_level -= (reprogramming * 0.6)
            self.epigenetic_status -= (reprogramming * 0.3)
            print(f"   -> 🧬 HSC REPROGRAMMING: Stellate cells deactivating ({self.hsc_activation_level:.2f})")

        elif "EGFR" in target and intervention.target.action == "ACTIVATE":
            # Objetivo: Estimular la regeneración de Hepatocitos
            self.hepatocyte_viability += (affinity * 0.2)
            print("   -> 🌱 REGENERATION: Stimulating hepatocyte proliferation.")

        # Penalización por Inmunogenicidad (Toxicidad)
        if intervention.immunogenicity_score > 0.4:
            self.hepatocyte_viability -= (intervention.immunogenicity_score * 0.2)

        self._clamp_values()
        return self.get_status()

    def update_state(self):
        self.steps += 1
        
        # La fibrosis crece si las HSCs están activas
        if self.hsc_activation_level > 0.3:
            self.fibrosis_level += 0.01 * self.hsc_activation_level
        else:
            # Si logramos "dormir" a las HSCs, el cuerpo limpia la fibrosis
            self.fibrosis_level -= 0.005
            self.hepatocyte_viability += 0.002

        self._clamp_values()

    def _clamp_values(self):
        self.fibrosis_level = max(0.0, min(1.0, self.fibrosis_level))
        self.hsc_activation_level = max(0.0, min(1.0, self.hsc_activation_level))
        self.hepatocyte_viability = max(0.0, min(1.0, self.hepatocyte_viability))
        self.epigenetic_status = max(0.0, min(1.0, self.epigenetic_status))

    def get_status(self):
        return {
            "step": self.steps,
            "fibrosis_index": round(self.fibrosis_level, 4),
            "hsc_activation": round(self.hsc_activation_level, 4),
            "hepatocyte_viability": round(self.hepatocyte_viability, 4),
            "epigenetic_status": round(self.epigenetic_status, 4)
        }
