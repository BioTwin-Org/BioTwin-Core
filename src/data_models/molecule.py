from dataclasses import dataclass
from typing import Optional

@dataclass
class HormokineStructure:
    pdb_content: str  # El contenido del archivo PDB en formato texto
    plddt_score: float # Métrica de confianza de ESMFold (0-100)
    molecular_weight: float
    is_folded: bool = False

@dataclass
class Hormokine:
    id: str
    sequence: str
    target_receptor: str
    structure: Optional[HormokineStructure] = None # Nueva capa 3D
    affinity_score: float = 0.0
