import requests
import random
# Importación absoluta correcta basada en la estructura del proyecto
from src.data_models.molecule import HormokineStructure

class BioNeMoService:
    """
    Cliente para interactuar con NVIDIA BioNeMo (o simularlo).
    """
    
    def fetch_esmfold_structure(self, sequence: str) -> HormokineStructure:
        """
        Genera una estructura 3D simulada (Mock) para evitar latencia en demos.
        """
        # PDB Header mínimo válido
        mock_pdb = "HEADER    MOCK STRUCTURE\nATOM      1  N   ALA A   1       0.000   0.000   0.000  1.00  0.00"
        return HormokineStructure(
            pdb_content=mock_pdb,
            plddt_score=90.0,
            molecular_weight=15.5
        )

    def get_real_cytokine_structure(self, pdb_id="1ALU"):
        """
        Recupera un PDB real de RCSB para visualización en el Dashboard.
        Esto asegura que el usuario vea una proteína bonita en pantalla.
        """
        url = f"https://files.rcsb.org/view/{pdb_id}.pdb"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return {
                    "pdb": response.text,
                    "score": 95.0,
                    "name": "Interleukin-6 Real Structure"
                }
        except Exception:
            pass
        return None
