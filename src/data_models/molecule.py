from dataclasses import dataclass
from typing import Optional

@dataclass
class HormokineStructure:
    pdb_content: str
    plddt_score: float
    molecular_weight: float
    is_folded: bool = True

@dataclass
class Hormokine:
    id: str
    name: str
    sequence: str
    target_receptor: str
    structure: Optional[HormokineStructure] = None
    affinity_score: float = 0.0
    instruction_potency: float = 0.9
    predicted_affinity: float = 0.9
