import random
from src.data_models.schemas import Hormokine

class LiverLobule:
    """
    Agent-based simulation of a Liver Lobule.
    Now supports structured Hormokine objects and receptor-specific logic.
    """
    def __init__(self, fibrosis_level=0.8):
        self.fibrosis_level = fibrosis_level # 0.0 (Healthy) to 1.0 (Cirrhosis)
        self.hepatocytes_health = 0.4
        self.steps = 0
        
        # Define the biological state of the tissue
        # In fibrosis, TGF-beta receptors are overexpressed
        self.surface_receptors = {
            "TGFBR2": {"expression": "high", "affinity_threshold": 0.8},
            "EGFR": {"expression": "normal", "affinity_threshold": 0.6}
        }

    def inject_treatment(self, intervention: Hormokine) -> dict:
        """
        Receives a structured Hormokine object.
        Validates targeting and calculates biological effect.
        """
        print(f"💉 [BioTwin] Injecting {intervention.intervention_id}...")
        
        # 1. Target Validation (Addressing Domain)
        target_receptor = intervention.target.receptor
        
        if target_receptor not in self.surface_receptors:
            print(f"   -> ❌ MISS: Tissue does not express receptor '{target_receptor}'.")
            return self.get_status()

        receptor_stats = self.surface_receptors[target_receptor]
        
        # 2. Affinity Check (Lock-and-Key Mechanism)
        # We use the predicted affinity from the AI model
        if intervention.predicted_affinity < receptor_stats["affinity_threshold"]:
            print(f"   -> ⚠️ BOUNCE: Affinity {intervention.predicted_affinity:.2f} too low for {target_receptor}.")
            return self.get_status()

        # 3. Calculate Efficacy based on Action
        # Ideally, we want an ANTAGONIST for TGF-beta (to stop fibrosis)
        effect_modifier = 0.0
        
        if target_receptor == "TGFBR2" and intervention.target.action == "INHIBIT":
            # Correct strategy: Inhibiting the fibrosis signal
            effect_modifier = 0.15 * intervention.predicted_affinity
            print("   -> ✅ MATCH: TGF-beta signal blocked. Fibrosis regressing.")
            
        elif target_receptor == "TGFBR2" and intervention.target.action == "ACTIVATE":
            # Wrong strategy: Activating fibrosis!
            effect_modifier = -0.10 
            print("   -> 💀 WARNING: Pro-fibrotic signal activated! Condition worsening.")
        
        else:
            print(f"   -> ℹ️ NEUTRAL: Bound to {target_receptor} but action '{intervention.target.action}' has no definition.")

        # 4. Apply Changes to State
        self.fibrosis_level -= effect_modifier
        
        # Enforce biological limits (0 to 1)
        self.fibrosis_level = max(0.0, min(1.0, self.fibrosis_level))
        
        # Side effect: Hepatocyte health improves if fibrosis goes down
        if effect_modifier > 0:
            self.hepatocytes_health += (effect_modifier * 0.5)

        self.update_state()
        return self.get_status()

    def update_state(self):
        """Advances time. Without treatment, fibrosis creeps back."""
        self.steps += 1
        if self.fibrosis_level > 0.2:
            self.fibrosis_level += 0.005 # Natural disease progression

    def get_status(self):
        return {
            "step": self.steps,
            "fibrosis_index": round(self.fibrosis_level, 4),
            "hepatocyte_viability": round(self.hepatocytes_health, 4)
        }
