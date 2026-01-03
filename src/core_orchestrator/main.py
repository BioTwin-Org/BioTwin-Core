import sys
import os

# Ensure Python can find the source modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.generative.bionemo_client import BioNeMoClient
from src.model_containers.agent_based.liver_model import LiverLobule

def run_simulation_pipeline():
    print("🚀 Starting BioTwin Core v0.2 (Logic Aware)...")
    print("==============================================")

    # 1. Initialize the Patient (Digital Twin)
    # This represents a liver with active fibrosis (High TGF-beta)
    patient = LiverLobule(fibrosis_level=0.90)
    print(f"🏥 Patient Status: {patient.get_status()}")

    # 2. Initialize AI Designer
    ai_designer = BioNeMoClient()

    # 3. Clinical Trial Simulation
    # Scenario: We need an inhibitor for TGFBR2
    
    print("\n--- 🧪 PHASE 1: GENERATION ---")
    # Let's ask the AI for a specific candidate
    candidate = ai_designer.generate_hormokine(
        target_receptor="TGFBR2", 
        effect="INHIBIT" 
    )
    print(f"Designed Molecule: {candidate.intervention_id}")
    print(f" > Sequence: {candidate.sequence[:10]}...")
    print(f" > Target: {candidate.target.receptor}")
    print(f" > Predicted Affinity: {candidate.predicted_affinity:.3f}")

    print("\n--- 💉 PHASE 2: INJECTION ---")
    # Direct object injection (Polymorphism in action)
    result = patient.inject_treatment(candidate)
    
    print("\n--- 📊 PHASE 3: REPORT ---")
    print(f"New Fibrosis Level: {result['fibrosis_index']}")
    
    if result['fibrosis_index'] < 0.90:
        print("✅ CLINICAL SUCCESS: The Hormokine successfully reprogrammed the tissue.")
    else:
        print("❌ FAILURE: Treatment was ineffective or affinity was too low.")

    print("==============================================")

if __name__ == "__main__":
    run_simulation_pipeline()
