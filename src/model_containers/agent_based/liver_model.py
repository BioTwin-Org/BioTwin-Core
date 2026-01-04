import random
from src.data_models.schemas import Hormokine

class LiverLobule:
    def __init__(self, fibrosis_level=0.8):
        self.fibrosis_level = fibrosis_level
        self.hepatocytes_health = 0.4
        self.steps = 0
        
        # --- NUEVAS VARIABLES EPIGENÉTICAS ---
        # 1.0 = Genes pro-fibrosis totalmente activos (mal estado)
        # 0.0 = Genes silenciados (reprogramación exitosa)
        self.epigenetic_fibrosis_driver = 1.0 
        
        self.surface_receptors = {
            "TGFBR2": {"expression": "high", "affinity_threshold": 0.8},
            "EGFR": {"expression": "normal", "affinity_threshold": 0.6}
        }

    def inject_treatment(self, intervention: Hormokine) -> dict:
        print(f"💉 [BioTwin] Injecting {intervention.intervention_id}...")
        
        target_receptor = intervention.target.receptor
        if target_receptor not in self.surface_receptors:
            print(f"   -> ❌ MISS: No target receptor found.")
            return self.get_status()

        # A. Fase de Direccionamiento (Addressing)
        affinity = intervention.predicted_affinity
        if affinity < self.surface_receptors[target_receptor]["affinity_threshold"]:
            print(f"   -> ⚠️ BOUNCE: Low affinity binding.")
            return self.get_status()

        # B. Fase de Instrucción Profunda (Epigenetic Reprogramming)
        # Aquí simulamos la 'carga útil' (payload) de la Hormokina
        if target_receptor == "TGFBR2" and intervention.target.action == "INHIBIT":
            # La instrucción reduce el driver epigenético de la enfermedad
            reprogramming_power = affinity * intervention.instruction_potency
            self.epigenetic_fibrosis_driver -= (reprogramming_power * 0.4)
            
            print(f"   -> 🧬 INSTRUCTION: Epigenetic silencing active. Driver down to {self.epigenetic_fibrosis_driver:.2f}")
            
            # El efecto inmediato en la fibrosis
            self.fibrosis_level -= (reprogramming_power * 0.2)
        
        self.update_state()
        return self.get_status()

    def update_state(self):
        self.steps += 1
        # La progresión natural de la enfermedad ahora está ligada al driver epigenético
        # Si logramos bajar el driver < 0.5, la fibrosis deja de crecer sola.
        if self.epigenetic_fibrosis_driver > 0.5:
            self.fibrosis_level += 0.01 * self.epigenetic_fibrosis_driver
        else:
            # Si el driver es bajo, hay regeneración espontánea
            self.fibrosis_level -= 0.005
            self.hepatocytes_health += 0.002

        self.fibrosis_level = max(0.0, min(1.0, self.fibrosis_level))
        self.epigenetic_fibrosis_driver = max(0.0, min(1.0, self.epigenetic_fibrosis_driver))

    def get_status(self):
        return {
            "step": self.steps,
            "fibrosis_index": round(self.fibrosis_level, 4),
            "epigenetic_status": round(self.epigenetic_fibrosis_driver, 4),
            "hepatocyte_viability": round(self.hepatocytes_health, 4)
        }
