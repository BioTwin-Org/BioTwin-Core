from dataclasses import dataclass
from typing import Optional

@dataclass
class HormokineStructure:
    """
    Datos físicos de la estructura 3D (Salida de ESMFold).
    """
    pdb_content: str       # Cadena de texto con formato PDB
    plddt_score: float     # Confianza del plegamiento (0-100)
    molecular_weight: float # Peso en kDa
    is_folded: bool = True

@dataclass
class Hormokine:
    """
    La entidad del fármaco diseñado.
    """
    id: str
    name: str
    sequence: str
    target_receptor: str
    structure: Optional[HormokineStructure] = None
    affinity_score: float = 0.0
    
    # Atributos para compatibilidad con el simulador
    instruction_potency: float = 0.9
    predicted_affinity: float = 0.9
