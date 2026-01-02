import sys
import os

# Ensure Python can find the source modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.generative.bionemo_client import BioNeMoClient
from src.model_containers.agent_based.liver_model import LiverLobule

def run_simulation_pipeline():
    print("🚀 Starting BioTwin Core v0.1 Alpha...")
    print("========================================")

    # 1. Initialize Digital Twin (Virtual Patient with Fibrosis)
    print("\n🏥 Initializing Liver Lobule Digital Twin...")
    patient_twin = LiverLobule(fibrosis_level=0.90) # Severe fibrosis
    print(f"   Initial State: {patient_twin.get_status()}")

    # 2. Initialize AI Engine
    ai_engine = BioNeMoClient() # Defaults to mock mode if no API key found

    # 3. Design and Treatment Loop
    # We will attempt to generate 3 different candidates
    for i in range(1, 4):
        print(f"\n🧪 --- Experimentation Cycle {i} ---")
        
        # A. Generate Hormokine
        candidate = ai_engine.generate_hormokine(
            target_receptor="TGFBR2", 
            effect="INHIBIT"
        )
        print(f"   Candidate Generated: {candidate['sequence'][:10]}... (ID: {candidate['sequence_id']})")

        # B. Simulate Injection into Twin
        outcome = patient_twin.inject_treatment(candidate)
        
        # C. Read Results
        print(f"   Clinical Result: Current Fibrosis = {outcome['fibrosis_index']}")

        if outcome['fibrosis_index'] < 0.7:
            print("\n🎉 SUCCESS! Significant fibrosis reversal observed.")
            break

    print("\n========================================")
    print("🏁 Simulation finished.")

if __name__ == "__main__":
    run_simulation_pipeline()