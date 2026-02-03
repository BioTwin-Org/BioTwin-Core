from dataclasses import dataclass
from typing import Optional

@dataclass
class HormokineStructure:
    """
    Representa el resultado físico del plegamiento de proteínas (ESMFold).
    Contiene los datos binarios del PDB y las métricas de calidad.
    """
    pdb_content: str       # El string del archivo .pdb para el renderizador
    plddt_score: float     # Confianza del modelo (0-100)
    molecular_weight: float # En kiloDaltons (kDa)
    is_folded: bool = False

@dataclass
class Hormokine:
    """
    Entidad principal de dominio.
    Representa el candidato terapéutico diseñado por la IA Generativa.
    """
    id: str
    name: str
    sequence: str          # Secuencia de aminoácidos (String)
    target_receptor: str   # Ej: TGFBR2, IL-6R
    structure: Optional[HormokineStructure] = None
    affinity_score: float = 0.0
