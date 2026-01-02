from dataclasses import dataclass, field
from typing import List, Optional
import json
import uuid
from datetime import datetime

@dataclass
class Domain:
    domain_type: str  # 'addressing', 'instruction', etc.
    start_pos: int
    end_pos: int
    description: str

@dataclass
class TargetProfile:
    cell_type: str
    receptor: str
    action: str  # 'agonist', 'antagonist'

@dataclass
class Hormokine:
    """
    Python representation of the Intervention Schema.
    Validates the structure of a synthetic molecule.
    """
    sequence: str
    target: TargetProfile
    molecule_type: str = "protein"
    intervention_id: str = field(default_factory=lambda: f"HK-{uuid.uuid4().hex[:8].upper()}")
    domains: List[Domain] = field(default_factory=list)
    predicted_affinity: float = 0.0
    immunogenicity_score: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_json(self):
        """Exports the object to a standard JSON string matching the schema."""
        return json.dumps({
            "intervention_id": self.intervention_id,
            "molecule_type": self.molecule_type,
            "sequence_data": {
                "primary_sequence": self.sequence
            },
            "target_profile": {
                "cell_type": self.target.cell_type,
                "receptor_target": self.target.receptor,
                "expected_action": self.target.action
            },
            "predicted_properties": {
                "binding_affinity_kd": self.predicted_affinity,
                "immunogenicity_score": self.immunogenicity_score
            },
            "architecture": [
                {
                    "domain_type": d.domain_type,
                    "start_pos": d.start_pos,
                    "end_pos": d.end_pos,
                    "function_description": d.description
                } for d in self.domains
            ]
        }, indent=2)

    @classmethod
    def from_dict(cls, data: dict):
        """Factory method to create a Hormokine from a dictionary."""
        target_data = data.get("target_profile", {})
        target = TargetProfile(
            cell_type=target_data.get("cell_type", "unknown"),
            receptor=target_data.get("receptor_target", "unknown"),
            action=target_data.get("expected_action", "unknown")
        )
        
        # Parse logic for domains would go here
        
        return cls(
            intervention_id=data.get("intervention_id"),
            molecule_type=data.get("molecule_type", "protein"),
            sequence=data.get("sequence_data", {}).get("primary_sequence", ""),
            target=target,
            predicted_affinity=data.get("predicted_properties", {}).get("binding_affinity_kd", 0.0)
        )
