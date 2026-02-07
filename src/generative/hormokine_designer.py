import random
from src.generative.bionemo_service import BioNeMoService
from src.data_models.molecule import Hormokine, HormokineStructure

class HormokineDesigner:
    def __init__(self):
        self.bionemo = BioNeMoService()

    def design_batch(self, target, mechanism, genotype, n=5):
        return [self.design_candidate(target, mechanism, genotype) for _ in range(n)]

    def design_candidate(self, target_receptor: str, action: str, patient_profile: any = None) -> Hormokine:
        variant = random.choice(["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "theta"])
        name = f"Hormokine-{target_receptor}-{variant}"
        
        # --- LÓGICA DE RIESGO ROBUSTA ---
        risk = 1.0
        if patient_profile:
            if hasattr(patient_profile, 'calculate_risk_factor'):
                risk = patient_profile.calculate_risk_factor()
            else:
                try:
                    risk = float(patient_profile)
                except (ValueError, TypeError):
                    risk = 1.0
        
        sequence = "".join(random.choices("ACDEFGHIKLMNPQRSTVWY", k=random.randint(40, 60)))
        structure = self.bionemo.fetch_esmfold_structure(sequence)
        
        return Hormokine(
            id=f"{target_receptor}-{variant}",
            name=name,
            sequence=sequence,
            target_receptor=target_receptor,
            structure=structure,
            instruction_potency=random.uniform(0.4, 0.8) * risk,
            predicted_affinity=random.uniform(0.7, 0.98)
        )
