from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class GenomicVariant:
    """
    Representa un SNP (Single Nucleotide Polymorphism) específico.
    """
    rsid: str                # ID estándar (ej: rs1800795)
    gene: str                # Gen afectado (ej: IL6)
    impact_score: float      # Factor de riesgo (1.0 = Neutro, >1.0 = Alto Riesgo)
    description: Optional[str] = None

@dataclass
class PatientGenotype:
    """
    El perfil genómico del Gemelo Digital.
    """
    patient_id: str
    variants: List[GenomicVariant] = field(default_factory=list)

    def calculate_risk_factor(self) -> float:
        """Calcula el riesgo acumulado basado en las variantes."""
        risk = 1.0
        for variant in self.variants:
            risk *= variant.impact_score
        return round(risk, 2)