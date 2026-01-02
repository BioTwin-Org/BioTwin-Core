import os
import random
import time
from src.data_models.schemas import Hormokine, TargetProfile

class BioNeMoClient:
    """
    Client for interacting with the NVIDIA BioNeMo Service.
    Acts as the 'Hormokine Designer' using Generative AI.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("NGC_API_KEY")
        # Falls back to simulation mode if no key provided
        self.mock_mode = not self.api_key

    def generate_hormokine(self, target_receptor: str, effect: str) -> Hormokine:
        """
        Generates a candidate protein sequence based on the therapeutic target.
        Returns a structured Hormokine object.
        """
        print(f"🤖 [AI Engine] Designing Hormokine for: {target_receptor} ({effect})...")
        
        if self.mock_mode:
            return self._mock_generation(target_receptor, effect)
        
        # Real call to NVIDIA NGC API (ESM-2 / ProtGPT2) would go here
        return self._mock_generation(target_receptor, effect)

    def _mock_generation(self, target_receptor, effect) -> Hormokine:
        """Generates realistic mock data using the official Schema."""
        time.sleep(1)  # Simulate inference latency
        
        # 1. Generate Mock Sequence
        amino_acids = "ACDEFGHIKLMNPQRSTVWY"
        sequence = "".join(random.choices(amino_acids, k=25))
        affinity = random.uniform(0.7, 0.99)
        
        # 2. Create the Target Profile Object
        # We assume hepatocytes for this default mock
        target_profile = TargetProfile(
            cell_type="hepatocyte",
            receptor=target_receptor,
            action=effect
        )

        # 3. Return the fully structured Hormokine Object
        # This uses the class we imported, satisfying the Linter
        return Hormokine(
            sequence=sequence,
            target=target_profile,
            predicted_affinity=affinity,
            molecule_type="protein"
        )
