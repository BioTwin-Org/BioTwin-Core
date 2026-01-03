import pytest
from src.model_containers.agent_based.liver_model import LiverLobule
from src.data_models.schemas import Hormokine, TargetProfile

def test_fibrosis_reduction():
    """
    Test that a valid Hormokine actually reduces fibrosis.
    This validates the 'Programming' aspect of the tissue.
    """
    # 1. Setup: Sick liver
    liver = LiverLobule(fibrosis_level=0.9)
    
    # 2. Action: Create a perfect drug manually
    perfect_drug = Hormokine(
        sequence="AAAAA",
        molecule_type="peptide",
        predicted_affinity=0.95, # Very high affinity
        target=TargetProfile(
            cell_type="hepatocyte",
            receptor="TGFBR2",     # Correct receptor
            action="INHIBIT"       # Correct action
        )
    )
    
    # 3. Inject
    result = liver.inject_treatment(perfect_drug)
    
    # 4. Assert: Fibrosis should decrease
    # Initial 0.9 - (0.15 * 0.95) + progression... should be < 0.9
    assert result['fibrosis_index'] < 0.9, "Fibrosis did not decrease with perfect treatment"

def test_wrong_receptor():
    """
    Test that targeting a non-existent receptor does nothing.
    Validates the 'Addressing Domain' logic.
    """
    liver = LiverLobule(fibrosis_level=0.9)
    
    useless_drug = Hormokine(
        sequence="BBBBB",
        target=TargetProfile(cell_type="brain", receptor="DOPAMINE_R", action="ACTIVATE"),
        predicted_affinity=0.99
    )
    
    result = liver.inject_treatment(useless_drug)
    
    # Fibrosis should increase slightly due to natural progression, not decrease
    assert result['fibrosis_index'] >= 0.9, "Treatment for wrong receptor should not cure fibrosis"
