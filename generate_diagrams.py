import base64
import requests
import os

diagrams = {
    "title_diagram": """
    graph TB
        subgraph "EventSync-AI Orchestrator"
        T[Title: Corporate Event Logistics Agent]
        S[Subtitle: Autonomous Multi-Agent Coordination with Human-in-the-Loop Approval]
        style T fill:#f96,stroke:#333,stroke-width:4px
        style S fill:#fff,stroke:#333,stroke-dasharray: 5 5
        end
    """,
    "architecture_diagram": """
    graph TD
        User((User)) --> Streamlit[Streamlit HITL Dashboard]
        Streamlit --> LG[LangGraph Orchestrator]
        subgraph Agents
        P[Planner Node]
        C[Coordinator Node]
        B[Budget Manager]
        E[Executive Node]
        end
        LG --> P
        LG --> C
        LG --> B
        LG --> E
        subgraph Tools
        V[Venue API]
        F[Catering API]
        A[AV Services API]
        end
        C --> V
        C --> F
        C --> A
    """,
    "sequence_diagram": """
    sequenceDiagram
        participant U as User
        participant A as Planner Agent
        participant C as Coordinator
        participant B as Budget Manager
        participant E as Executive

        U->>A: Specify Event Requirements
        A->>C: Request Logistics Options
        C->>C: Query Venue & Catering
        C->>B: Submit Selection & Costs
        B-->>U: Request Approval (Threshold > $15k)
        U->>B: Approved
        B->>E: Authorize Contracts
        E-->>U: Final Logistics Report
    """,
    "flow_diagram": """
    flowchart TD
        Start([Start]) --> Plan[Generate Logistics Plan]
        Plan --> Research[Research Vendors & Quotes]
        Research --> Calc[Calculate Total Budget]
        Calc --> Check{Budget > $15k?}
        Check -- Yes --> Approval[Wait for Human Approval]
        Approval --> Exec[Execute Contracts]
        Check -- No --> Exec
        Exec --> Report[Generate Final Report]
        Report --> End([End])
    """
}

os.makedirs("images", exist_ok=True)

for name, code in diagrams.items():
    encoded = base64.b64encode(code.encode()).decode()
    url = f"https://mermaid.ink/img/{encoded}"
    print(f"Generating {name}...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"images/{name}.png", 'wb') as f:
            f.write(response.content)
        print(f"Successfully saved images/{name}.png")
    else:
        print(f"Failed to generate {name}. Status code: {response.status_code}")
