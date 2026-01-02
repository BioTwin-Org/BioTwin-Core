class LiverLobule:
    """
    Simplified agent-based simulation of a Liver Lobule.
    Initial State: Induced Fibrosis.
    """
    def __init__(self, fibrosis_level=0.8):
        self.fibrosis_level = fibrosis_level # 0.0 (Healthy) to 1.0 (Cirrhosis)
        self.hepatocytes_health = 0.4
        self.steps = 0

    def inject_treatment(self, molecule: dict):
        """
        Receives a 'Hormokine' and simulates its effect on the tissue logic.
        """
        seq_name = molecule.get("sequence_id", "Unknown")
        affinity = molecule.get("predicted_affinity", 0)
        
        print(f"💉 [BioTwin] Injecting {seq_name} (Affinity: {affinity:.2f})")
        
        # Simple simulation logic:
        # High affinity (>0.85) triggers signaling pathways to reduce fibrosis.
        # Low affinity results in negligible effect or potential toxicity.
        
        if affinity > 0.85:
            effectiveness = (affinity - 0.8) * 2  # Impact factor
            self.fibrosis_level -= effectiveness
            self.hepatocytes_health += (effectiveness * 0.5)
            print("   -> ✅ Therapeutic Effect detected: Regeneration pathway activated.")
        else:
            print("   -> ⚠️ Low Affinity: Treatment failed to bind target receptor effectively.")
            
        # Clamp values to realistic physical ranges
        self.fibrosis_level = max(0.0, min(1.0, self.fibrosis_level))
        self.update_state()
        
        return self.get_status()

    def update_state(self):
        """Advances the simulation by one time step."""
        self.steps += 1
        # Natural dynamics: without treatment, disease progresses slowly
        if self.fibrosis_level > 0.3:
            self.fibrosis_level += 0.01 

    def get_status(self):
        return {
            "step": self.steps,
            "fibrosis_index": round(self.fibrosis_level, 4),
            "hepatocyte_viability": round(self.hepatocytes_health, 4)
        }