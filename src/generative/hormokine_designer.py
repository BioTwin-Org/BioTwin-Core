from src.generative.bionemo_service import BioNeMoService
from src.data_models.molecule import Hormokine, HormokineStructure
from src.data_models.genomics import PatientGenotype

class HormokineDesigner:
    def __init__(self):
        self.bionemo = BioNeMoService()
    def design_batch(self, target, mechanism, genotype, n=5):
         return [self._generate_one(target, mechanism, genotype) for _ in range(n)]

    def design_candidate(self, target_receptor: str, action: str, patient_profile: PatientGenotype = None) -> Hormokine:
        """
        Diseña una Hormokina personalizada. 
        Si se entrega un patient_profile, ajusta la potencia según el riesgo genético.
        """
        # 1. Selección de Secuencia Base (Simulada)
        base_sequences = {
            "TGFBR2": "MAGSLLRGSLLLLL", # Target Fibrosis
            "IL-6R":  "MVLAQGLLVPLLLL", # Target Inflamación
            "EGFR":   "MRPSGTAGAALLAL"  # Target Regeneración
        }
        sequence = base_sequences.get(target_receptor, "ACDEFGHIKLMNPQRST")

        # 2. Ajuste por Genómica (Medicina de Precisión)
        potency = 0.85
        if patient_profile:
            risk = patient_profile.calculate_risk_factor()
            if risk > 1.2:
                # Si el paciente es de alto riesgo, diseñamos una molécula más potente
                potency = 0.98
                sequence += "RRR" # Modificación ficticia para aumentar afinidad

        # 3. Plegamiento 3D (BioNeMo ESMFold)
        structure = self.bionemo.fetch_esmfold_structure(sequence)

        return Hormokine(
            id=f"HK-{target_receptor[:3]}-001",
            name=f"Anti-{target_receptor} Aptamer",
            sequence=sequence,
            target_receptor=target_receptor,
            structure=structure,
            affinity_score=potency, # Mapeamos potencia a afinidad para simplificar
            instruction_potency=potency,
            predicted_affinity=potency

        )
