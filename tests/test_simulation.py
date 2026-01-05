import pytest
from src.model_containers.agent_based.liver_model import LiverLobule
from src.data_models.schemas import Hormokine, TargetProfile

def test_hsc_reprogramming_and_epigenetics():
    """
    Validates that TGFBR2 inhibition reduces both HSC activation 
    and the epigenetic driver.
    """
    liver = LiverLobule(fibrosis_level=0.9)
    status_before = liver.get_status()
    
    # Create a potent inhibitor
    treatment = Hormokine(
        sequence="TEST-SEQ-HSC",
        predicted_affinity=0.9,
        instruction_potency=1.0,
        target=TargetProfile(cell_type="stellate", receptor="TGFBR2", action="INHIBIT")
    )
    
    status_after = liver.inject_treatment(treatment)
    
    assert status_after['hsc_activation'] < status_before['hsc_activation']
    assert status_after['epigenetic_status'] < status_before['epigenetic_status']

def test_hepatocyte_viability_increase():
    """
    Validates that EGFR activation improves hepatocyte viability.
    """
    liver = LiverLobule(fibrosis_level=0.5)
    status_before = liver.get_status()
    
    regen_hormokine = Hormokine(
        sequence="TEST-SEQ-REGEN",
        predicted_affinity=0.8,
        target=TargetProfile(cell_type="hepatocyte", receptor="EGFR", action="ACTIVATE")
    )
    
    status_after = liver.inject_treatment(regen_hormokine)
    
    assert status_after['hepatocyte_viability'] > status_before['hepatocyte_viability']

def test_boundary_conditions():
    """
    Ensures that values stay within the [0, 1] biological range.
    """
    liver = LiverLobule(fibrosis_level=0.05)
    # Injecting a very strong drug to try and force negative values
    super_drug = Hormokine(
        sequence="OVERPOWERED",
        predicted_affinity=1.0,
        instruction_potency=1.0,
        target=TargetProfile(cell_type="stellate", receptor="TGFBR2", action="INHIBIT")
    )
    
    result = liver.inject_treatment(super_drug)
    assert 0.0 <= result['fibrosis_index'] <= 1.0
    assert 0.0 <= result['hsc_activation'] <= 1.0
