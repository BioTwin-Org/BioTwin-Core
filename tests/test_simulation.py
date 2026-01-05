import pytest
from src.model_containers.agent_based.liver_model import LiverLobule
from src.data_models.schemas import Hormokine, TargetProfile

def test_hsc_reprogramming_success():
    """
    Test that targeting TGFBR2 successfully deactivates Stellate Cells (HSCs).
    """
    # 1. Setup: Liver with 100% active HSCs
    liver = LiverLobule(fibrosis_level=0.9)
    initial_hsc_status = liver.get_status()['hsc_activation']
    
    # 2. Action: Create an 'Inhibitor' Hormokine for TGFBR2
    treatment = Hormokine(
        sequence="ANTI-FIBROSIS-001",
        predicted_affinity=0.9,
        instruction_potency=0.9,
        target=TargetProfile(
            cell_type="hepatocyte", # Or stellate, logic handles TGFBR2
            receptor="TGFBR2",
            action="INHIBIT"
        )
    )
    
    # 3. Inject
    result = liver.inject_treatment(treatment)
    
    # 4. Assert: HSC activation must drop
    assert result['hsc_activation'] < initial_hsc_status
    assert result['epigenetic_status'] < 1.0

def test_hepatocyte_regeneration():
    """
    Test that targeting EGFR promotes hepatocyte viability.
    """
    liver = LiverLobule(fibrosis_level=0.5)
    initial_health = liver.get_status()['hepatocyte_viability']
    
    regen_hormokine = Hormokine(
        sequence="REGEN-001",
        predicted_affinity=0.8,
        target=TargetProfile(cell_type="hepatocyte", receptor="EGFR", action="ACTIVATE")
    )
    
    result = liver.inject_treatment(regen_hormokine)
    
    # 5. Assert: Viability should increase
    assert result['hepatocyte_viability'] > initial_health

def test_clamping_logic():
    """
    Ensure values never go below 0.0 or above 1.0.
    """
    liver = LiverLobule(fibrosis_level=0.1)
    # Force an extremely potent treatment
    super_drug = Hormokine(
        sequence="SUPER",
        predicted_affinity=1.0,
        instruction_potency=1.0,
        target=TargetProfile(cell_type="hepatocyte", receptor="TGFBR2", action="INHIBIT")
    )
    
    # Inject multiple times
    for _ in range(5):
        result = liver.inject_treatment(super_drug)
        
    assert result['fibrosis_index'] >= 0.0
    assert result['hsc_activation'] >= 0.0
