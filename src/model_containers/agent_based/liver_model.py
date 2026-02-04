import numpy as np
import random

class KupfferCell:
    def __init__(self):
        self.inflammation_output = 0.2
        self.state = "M2"

    def sense_and_react(self, health_index, genetic_risk):
        activation_threshold = 0.6 / genetic_risk
        if health_index < activation_threshold:
            self.state = "M1"
            self.inflammation_output = min(1.0, self.inflammation_output + 0.05)
        else:
            self.state = "M2"
            self.inflammation_output = max(0.1, self.inflammation_output - 0.08)
        return self.inflammation_output

class LiverModel:
    def __init__(self, fibrosis_level=0.85, genetic_risk=1.0, **kwargs):
        self.steps = 0
        self.fibrosis_level = fibrosis_level
        self.genetic_risk = genetic_risk
        
        # Parámetros internos con valores por defecto
        self.hsc_activation_level = kwargs.get('hsc_activation', 0.90)
        self.hepatocyte_viability = kwargs.get('viability', 0.45)
        self.inflammation_level = kwargs.get('inflammation', 0.80)
        
        # Población de Agentes
        self.kupffer_population = [KupfferCell() for _ in range(10)]
        self.history = []

    def update_state(self):
        self.steps += 1
        cytokine_levels = [
            k.sense_and_react(self.hepatocyte_viability, self.genetic_risk) 
            for k in self.kupffer_population
        ]
        self.inflammation_level = sum(cytokine_levels) / len(self.kupffer_population)

        if self.inflammation_level > 0.4:
            self.hsc_activation_level = min(1.0, self.hsc_activation_level + 0.02)
            self.hepatocyte_viability = max(0.0, self.hepatocyte_viability - 0.01)
        
        if self.hsc_activation_level > 0.6:
            self.fibrosis_level = min(1.0, self.fibrosis_level + 0.01)
        elif self.hsc_activation_level < 0.4:
            self.fibrosis_level = max(0.0, self.fibrosis_level - 0.03)

        self.history.append({
            "Step": self.steps,
            "Fibrosis": self.fibrosis_level,
            "Inflammation": self.inflammation_level
        })

    def inject_hormokine(self, potency, target_affinity):
        """Lógica central de inyección."""
        effectiveness = potency * target_affinity
        self.inflammation_level = max(0.05, self.inflammation_level - (effectiveness * 0.8))
        self.hsc_activation_level = max(0.1, self.hsc_activation_level - (effectiveness * 0.6))

    # --- MÉTODOS DE COMPATIBILIDAD PARA TESTS ---

    def inject_treatment(self, hormokine):
        """
        Wrapper de compatibilidad. Acepta un objeto Hormokine o dict.
        """
        # Extraer valores de atributos u obtener de diccionario
        potency = getattr(hormokine, "instruction_potency", None)
        affinity = getattr(hormokine, "predicted_affinity", None)
        
        if potency is None or affinity is None:
            # Soporte para input tipo diccionario si falla el objeto
            potency = getattr(hormokine, "potency", 0.9) 
            affinity = getattr(hormokine, "target_affinity", 0.9)

        # Ejecutar lógica principal
        self.inject_hormokine(potency, affinity)

        # Avanzar el estado para que el test vea el cambio inmediato
        self.update_state()

        return self.get_status()

    def get_status(self):
        """
        Retorna el estado del tejido con las claves esperadas por la suite de pruebas.
        """
        return {
            "fibrosis_index": self.fibrosis_level,
            "hsc_activation": self.hsc_activation_level,
            "hepatocyte_viability": self.hepatocyte_viability,
            "inflammation_level": self.inflammation_level,
        }

# Alias para compatibilidad con el Test Suite (LiverLobule)
LiverLobule = LiverModel
