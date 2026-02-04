from dataclasses import dataclass, field
from typing import List

@dataclass
class GenomicVariant:
    """
    Representa una mutación puntual (SNP) identificada por AlphaGenome.
    """
    gene_symbol: str         # Ej: "IL6", "TGFB1"
    rsid: str                # ID estándar de la variante (ej. rs1800795)
    description: str         # Descripción clínica (ej. "Promoter region variant")
    penetrance_factor: float # Multiplicador de impacto en la simulación (1.0 = Neutro)

@dataclass
class PatientProfile:
    """
    El perfil genómico del Gemelo Digital.
    Contiene la lista de variantes activas para un paciente específico.
    """
    patient_id: str
    variants: List[GenomicVariant] = field(default_factory=list)

    def calculate_cumulative_risk(self) -> float:
        """
        Calcula el factor de riesgo total combinando todas las variantes.
        Utilizado por LiverModel para ajustar la agresividad de la inflamación.
        """
        risk_multiplier = 1.0
        for variant in self.variants:
            risk_multiplier *= variant.penetrance_factor
        return round(risk_multiplier, 2)
