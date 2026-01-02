import sys
import os

# Ensure Python can find the source modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.generative.bionemo_client import BioNeMoClient
from src.model_containers.agent_based.liver_model import LiverLobule

def run_simulation_pipeline():
    print("🚀 Starting BioTwin Core v0.1 Alpha...")
    print("========================================")

    # 1. Initialize Digital Twin
    print("\n🏥 Initializing Liver Lobule Digital Twin...")
    patient_twin = LiverLobule(fibrosis_level=0.90)
    print(f"   Initial State: {patient_twin.get_status()}")

    # 2. Initialize AI Engine
    ai_engine = BioNeMoClient()

    # 3. Design and Treatment Loop
    for i in range(1, 4):
        print(f"\n🧪 --- Experimentation Cycle {i} ---")
        
        # A. Generate Hormokine (Now returns an Object, not a dict)
        candidate_obj = ai_engine.generate_hormokine(
            target_receptor="TGFBR2", 
            effect="INHIBIT"
        )
        # Access attributes with dot notation (.) instead of brackets ['']
        print(f"   Candidate Generated: {candidate_obj.sequence[:10]}... (ID: {candidate_obj.intervention_id})")

        # B. Simulate Injection (We need to convert back to dict or update liver model)
        # For simplicity now, let's pass the full object to the updated liver model
        # NOTE: Using .__dict__ is a quick hack for compatibility with the old liver model
        # Ideally, we update liver_model.py to accept objects too.
        outcome = patient_twin.inject_treatment(candidate_obj.__dict__)
        
        # C. Read Results
        print(f"   Clinical Result: Current Fibrosis = {outcome['fibrosis_index']}")

        if outcome['fibrosis_index'] < 0.7:
            print("\n🎉 SUCCESS! Significant fibrosis reversal observed.")
            break

    print("\n========================================")
    print("🏁 Simulation finished.")

if __name__ == "__main__":
    run_simulation_pipeline()
