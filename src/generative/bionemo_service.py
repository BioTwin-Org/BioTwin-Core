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
        mock_pdb = (
            "HEADER    BIO-TWIN GENERATED STRUCTURE\n"
            "ATOM      1  N   ALA A   1      -0.528   1.511   0.000  1.00  0.00           N\n"
            "ATOM      2  CA  ALA A   1       0.000   0.000   0.000  1.00  0.00           C\n"
        )
        
        return HormokineStructure(
            pdb_content=mock_pdb,
            plddt_score=88.5,
            molecular_weight=24.5,
            is_folded=True
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
