import os
from dotenv import load_dotenv
from agents import create_graph

load_dotenv()

def run_simulation():
    print("=== EventSync-AI: Corporate Event Logistics Orchestrator ===")
    print("System: Initializing multi-agent workflow...")
    
    app = create_graph()
    
    initial_state = {
        "messages": [],
        "plan": {},
        "budget_total": 0.0,
        "confirmed_items": [],
        "approval_required": False,
        "final_report": ""
    }
    
    print("\n[PROCESS] Planner Node: Designing event architecture...")
    final_output = app.invoke(initial_state)
    
    print("\n" + final_output["final_report"])
    print("=== Simulation Complete ===")

if __name__ == "__main__":
    run_simulation()
