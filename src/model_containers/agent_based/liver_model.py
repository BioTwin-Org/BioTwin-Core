import random
from src.data_models.schemas import Hormokine

class LiverLobule:
    """
    Agent-based simulation of a Liver Lobule.
    Implements advanced biological logic: Epigenetic Reprogramming, 
    Addressing Domains, and Inflammation-Triggered Release.
    """
    def __init__(self, fibrosis_level=0.8):
        self.fibrosis_level = fibrosis_level  # 0.0 (Healthy) to 1.0 (Cirrhosis)
        self.hepatocytes_health = 0.4
        self.steps = 0
        
        # --- EPIGENETIC STATE ---
        # Represents the activation of pro-fibrotic genes (e.g., Collagen Type I)
        # 1.0 = Fully Active / 0.0 = Silenced (Reprogrammed)
        self.epigenetic_fibrosis_driver = 1.0 
        
        # --- TISSUE RECEPTOR PROFILE ---
        self.surface_receptors = {
            "TGFBR2": {"expression": "high", "affinity_threshold": 0.8},
            "EGFR": {"expression": "normal", "affinity_threshold": 0.6}
        }

    def inject_treatment(self, intervention: Hormokine) -> dict:
        """
        Processes a structured Hormokine object through the biological logic gate.
        """
        print(f"💉 [BioTwin] Processing Treatment: {intervention.intervention_id}")
        
        # 1. INFLAMMATION SENSOR (Timing/Release Domain)
        # The Hormokine only activates if it detects pathological fibrosis levels (> 0.3)
        if self.fibrosis_level < 0.3:
            print("   -> ⏳ LATENT: Inflammation levels below activation threshold. Hormone remains inactive.")
            return self.get_status()

        # 2. ADDRESSING (Targeting Domain)
        target_receptor = intervention.target.receptor
        if target_receptor not in self.surface_receptors:
            print(f"   -> ❌ MISS: Receptor '{target_receptor}' not expressed in this tissue.")
            return self.get_status()

        receptor_stats = self.surface_receptors[target_receptor]
        
        # 3. BINDING AFFINITY (Lock-and-Key Mechanism)
        if intervention.predicted_affinity < receptor_stats["affinity_threshold"]:
            print(f"   -> ⚠️ BOUNCE: Affinity {intervention.predicted_affinity:.2f} too low for {target_receptor}.")
            return self.get_status()

        # 4. INSTRUCTIONAL PHASE (Epigenetic Payload)
        # If bound correctly, the 'Instruction Domain' delivers its molecular payload
        if target_receptor == "TGFBR2" and intervention.target.action == "INHIBIT":
            # Reprogramming power depends on both Affinity and Instruction Potency
            reprogramming_power = intervention.predicted_affinity * intervention.instruction_potency
            
            # Reduce the epigenetic driver of the disease
            self.epigenetic_fibrosis_driver -= (reprogramming_power * 0.45)
            print(f"   -> 🧬 REPROGRAMMING: Epigenetic driver silenced to {self.epigenetic_fibrosis_driver:.2f}")
            
            # Immediate therapeutic effect on physical tissue
            self.fibrosis_level -= (reprogramming_power * 0.2)
            
        elif target_receptor == "EGFR" and intervention.target.action == "ACTIVATE":
            # Direct regeneration pathway
            self.hepatocytes_health += 0.15
            print("   -> 🌱 REGENERATION: Activating hepatocyte proliferation pathway.")

        # Clamp values to biological physical limits
        self._clamp_values()
        
        self.update_state()
        return self.get_status()
        # 5. TOXICITY CHECK (Off-target damage)
        if intervention.immunogenicity_score > 0.45:
            # Si el puntaje es alto, hay una reacción inflamatoria secundaria
            toxicity_damage = intervention.immunogenicity_score * 0.25
            self.hepatocytes_health -= toxicity_damage
            print(f"   -> ⚠️ TOXICITY: Immune response detected. Viability hit: -{toxicity_damage:.2f}")

    def update_state(self):
        """
        Advances the simulation by one time step.
        Physiology is governed by the state of the Epigenetic Driver.
        """
        self.steps += 1
        
        # NATURAL DISEASE PROGRESSION
        # If the driver is > 0.5, the disease continues to progress
        if self.epigenetic_fibrosis_driver > 0.5:
            self.fibrosis_level += 0.008 * self.epigenetic_fibrosis_driver
        else:
            # If the driver is silenced (< 0.5), endogenous repair begins
            self.fibrosis_level -= 0.004
            self.hepatocytes_health += 0.003

        self._clamp_values()

    def _clamp_values(self):
        """Ensures biological indices stay within 0.0 and 1.0."""
        self.fibrosis_level = max(0.0, min(1.0, self.fibrosis_level))
        self.epigenetic_fibrosis_driver = max(0.0, min(1.0, self.epigenetic_fibrosis_driver))
        self.hepatocytes_health = max(0.0, min(1.0, self.hepatocytes_health))

    def get_status(self):
        """Returns the current physiological state of the Twin."""
        return {
            "step": self.steps,
            "fibrosis_index": round(self.fibrosis_level, 4),
            "epigenetic_status": round(self.epigenetic_fibrosis_driver, 4),
            "hepatocyte_viability": round(self.hepatocytes_health, 4)
        }


