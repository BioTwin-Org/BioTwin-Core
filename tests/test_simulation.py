import pytest
from src.model_containers.agent_based.liver_model import LiverLobule
from src.data_models.schemas import Hormokine, TargetProfile

def test_hsc_inhibition_pathway():
    """
    Validates that a TGFBR2 inhibitor reduces HSC activation.
    """
    # Start with high activation
    liver = LiverLobule(fibrosis_level=0.8)
    initial_hsc = liver.get_status()['hsc_activation']
    
    # Create a potent Hormokine
    treatment = Hormokine(
        sequence="ANTI-FIB-TEST",
        predicted_affinity=0.95,
        instruction_potency=1.0,
        target=TargetProfile(cell_type="stellate", receptor="TGFBR2", action="INHIBIT")
    )
    
    # Inject and check immediate response
    status = liver.inject_treatment(treatment)
    
    # Check if HSC activation decreased
    assert status['hsc_activation'] < initial_hsc, f"HSC did not drop: {status['hsc_activation']} vs {initial_hsc}"

def test_hepatocyte_regeneration_pathway():
    """
    Validates that an EGFR activator improves viability.
    """
    liver = LiverLobule(fibrosis_level=0.5)
    initial_health = liver.get_status()['hepatocyte_viability']
    
    regen = Hormokine(
        sequence="REGEN-TEST",
        predicted_affinity=0.9,
        target=TargetProfile(cell_type="hepatocyte", receptor="EGFR", action="ACTIVATE")
    )
    
    status = liver.inject_treatment(regen)
    
    assert status['hepatocyte_viability'] > initial_health, "Viability did not increase"

def test_biological_bounds():
    """
    Ensures values stay within 0.0 and 1.0.
    """
    liver = LiverLobule(fibrosis_level=0.9)
    # Test extreme drug
    god_drug = Hormokine(
        sequence="MAX-POWER",
        predicted_affinity=1.0,
        instruction_potency=1.0,
        target=TargetProfile(cell_type="stellate", receptor="TGFBR2", action="INHIBIT")
    )
    
    # Apply multiple times
    for _ in range(10):
        res = liver.inject_treatment(god_drug)
    
    assert 0.0 <= res['fibrosis_index'] <= 1.0
    assert 0.0 <= res['hsc_activation'] <= 1.0
    assert 0.0 <= res['hepatocyte_viability'] <= 1.0
