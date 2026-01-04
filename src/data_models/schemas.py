from dataclasses import dataclass, field
from typing import List
import json
import uuid
from datetime import datetime

@dataclass
class Domain:
    domain_type: str  # 'addressing', 'instruction', 'timing', 'penetration'
    start_pos: int
    end_pos: int
    description: str

@dataclass
class TargetProfile:
    cell_type: str
    receptor: str
    action: str  # 'agonist', 'antagonist', 'INHIBIT', 'ACTIVATE'

@dataclass
class Hormokine:
    """
    Python representation of the Intervention Schema.
    Now includes 'instruction_potency' for epigenetic reprogramming.
    """
    sequence: str
    target: TargetProfile
    molecule_type: str = "protein"
    intervention_id: str = field(default_factory=lambda: f"HK-{uuid.uuid4().hex[:8].upper()}")
    domains: List[Domain] = field(default_factory=list)
    predicted_affinity: float = 0.0
    instruction_potency: float = 0.8  # Default value for deep reprogramming
    immunogenicity_score: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_json(self):
        """Exports the object to a standard JSON string matching the schema."""
        return json.dumps({
            "intervention_id": self.intervention_id,
            "molecule_type": self.molecule_type,
            "sequence_data": {"primary_sequence": self.sequence},
            "target_profile": {
                "cell_type": self.target.cell_type,
                "receptor_target": self.target.receptor,
                "expected_action": self.target.action
            },
            "predicted_properties": {
                "binding_affinity_kd": self.predicted_affinity,
                "instruction_potency": self.instruction_potency,
                "immunogenicity_score": self.immunogenicity_score
            }
        }, indent=2)
