import numpy as np

class KupfferCell:
    def __init__(self):
        self.inflammation_output = 0.5
        self.is_polarized_M1 = True 

    def react(self, health, hsc_act):
        # Si la salud cae o la activación sube, se inflama más (M1)
        if health < 0.5 or hsc_act > 0.6:
            self.is_polarized_M1 = True
            self.inflammation_output = min(1.0, self.inflammation_output + 0.08)
        else:
            self.is_polarized_M1 = False
            self.inflammation_output = max(0.05, self.inflammation_output - 0.05)
        return self.inflammation_output

class LiverModel:
    def __init__(self):
        self.steps = 0
        self.fibrosis_level = 0.85
        self.hsc_activation_level = 0.90
        self.hepatocyte_viability = 0.45
        self.inflammation_level = 0.80
        self.kupffer_cells = [KupfferCell() for _ in range(5)]
        self.history = []

    def update_state(self):
        self.steps += 1
        
        # 1. Las Kupffer reaccionan al microambiente
        self.inflammation_level = sum([k.react(self.hepatocyte_viability, self.hsc_activation_level) 
                                      for k in self.kupffer_cells]) / 5
        
        # 2. La inflamación impulsa la activación de HSC (Efecto cascada)
        if self.inflammation_level > 0.4:
            self.hsc_activation_level = min(1.0, self.hsc_activation_level + 0.02)
        
        # 3. Lógica de recuperación (Solo si la activación baja del umbral)
        if self.hsc_activation_level < 0.45:
            self.fibrosis_level = max(0.0, self.fibrosis_level - 0.04)
            self.hepatocyte_viability = min(1.0, self.hepatocyte_viability + 0.01)
        else:
            self.fibrosis_level = min(1.0, self.fibrosis_level + 0.01)

        self.history.append({
            "Step": self.steps,
            "Fibrosis": self.fibrosis_level,
            "HSC_Activation": self.hsc_activation_level,
            "Inflammation": self.inflammation_level,
            "Health": self.hepatocyte_viability
        })

    def inject_hormokine(self, potency):
        # La Hormokina ataca directamente la inflamación y la activación
        self.inflammation_level = max(0.1, self.inflammation_level - (potency * 0.7))
        self.hsc_activation_level = max(0.05, self.hsc_activation_level - (potency * 0.9))
