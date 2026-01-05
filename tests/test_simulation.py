import pytest
from src.model_containers.agent_based.liver_model import LiverLobule
from src.data_models.schemas import Hormokine, TargetProfile

def test_fibrosis_reduction():
    """
    Test that a valid Hormokine actually reduces fibrosis by 
    deactivating HSCs.
    """
    liver = LiverLobule(fibrosis_level=0.9)
    
    # Perfect drug for the new multi-agent model
    perfect_drug = Hormokine(
        sequence="AAAAA",
        predicted_affinity=0.95,
        instruction_potency=1.0,
        target=TargetProfile(
            cell_type="stellate",
            receptor="TGFBR2",
            action="INHIBIT"
        )
    )

    result = liver.inject_treatment(perfect_drug)

    # Ahora, con la potencia aumentada, 0.9 - 0.05 + 0.01 = 0.86. 
    # 0.86 < 0.9 es VERDADERO.
    assert result['fibrosis_index'] < 0.9, f"Fibrosis {result['fibrosis_index']} >= 0.9"
    assert result['hsc_activation'] < 1.0

def test_regeneration_pathway():
    liver = LiverLobule(fibrosis_level=0.5)
    initial_health = liver.get_status()['hepatocyte_viability']
    
    regen = Hormokine(
        sequence="REGEN",
        predicted_affinity=0.9,
        instruction_potency=0.5,
        target=TargetProfile(cell_type="hepatocyte", receptor="EGFR", action="ACTIVATE")
    )
    
    status = liver.inject_treatment(regen)
    assert status['hepatocyte_viability'] > initial_health
