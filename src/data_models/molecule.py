from dataclasses import dataclass
from typing import Optional

@dataclass
class HormokineStructure:
    """Estructura de datos para los resultados de plegamiento 3D (ESMFold)"""
    pdb_content: str
    plddt_score: float
    molecular_weight: float
    is_folded: bool = False

@dataclass
class Hormokine:
    """Entidad principal que representa la molécula diseñada por IA"""
    id: str
    sequence: str
    target_receptor: str
    structure: Optional[HormokineStructure] = None
    affinity_score: float = 0.0
