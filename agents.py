import operator
from typing import Annotated, TypedDict, List, Dict, Any, Union
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import tools

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    plan: Dict[str, Any]
    budget_total: float
    confirmed_items: List[Dict[str, Any]]
    approval_required: bool
    final_report: str

def planner_node(state: AgentState):
    """Initial planning node."""
    llm = ChatOpenAI(model="gpt-4o")
    # Simulate planning logic
    prompt = "Create a logistics plan for a corporate event: 200 people, NYC, 2 days. AV required."
    response = llm.invoke([HumanMessage(content=prompt)])
    
    # Mocked plan structure for the PoC
    plan = {
        "location": "New York City",
        "attendee_count": 200,
        "requirements": "High-end AV, Streaming, Premium Catering",
        "budget_limit": 25000
    }
    return {"plan": plan, "messages": [AIMessage(content="Generated initial event plan.")]}

def coordinator_node(state: AgentState):
    """Node for venue and catering research."""
    plan = state["plan"]
    venues = tools.get_venue_options(plan["location"], plan["attendee_count"])
    catering = tools.get_catering_quotes(plan["attendee_count"])
    
    # Simple selection logic: Best rating
    best_venue = sorted(venues, key=lambda x: x["rating"], reverse=True)[0]
    best_catering = sorted(catering, key=lambda x: x["rating"], reverse=True)[0]
    
    research_summary = f"Selected {best_venue['name']} and {best_catering['vendor']}."
    return {
        "messages": [AIMessage(content=research_summary)],
        "confirmed_items": [{"venue": best_venue}, {"catering": best_catering}]
    }

def budget_manager_node(state: AgentState):
    """Calculates total cost and checks if HITL is needed."""
    items = state["confirmed_items"]
    total = sum(i.get("venue", {}).get("price_per_day", 0) for i in items) + \
            sum(i.get("catering", {}).get("total_cost", 0) for i in items)
    
    approval_needed = total > 15000 # Threshold for PoC
    
    return {
        "budget_total": total,
        "approval_required": approval_needed,
        "messages": [AIMessage(content=f"Budget calculated: ${total}. Approval required: {approval_needed}")]
    }

def human_approval_node(state: AgentState):
    """Placeholder for human intervention."""
    return {"messages": [AIMessage(content="Waiting for human approval... (Simulated)")]}

def executive_node(state: AgentState):
    """Finalizes the booking."""
    items = state["confirmed_items"]
    report = "### EVENT FINALIZATION REPORT\n"
    for item in items:
        if "venue" in item:
            res = tools.finalize_booking({"item": item["venue"]["name"], "cost": item["venue"]["price_per_day"]})
            report += f"- Venue: {item['venue']['name']} (ID: {res['confirmation_id']})\n"
        if "catering" in item:
            res = tools.finalize_booking({"item": item["catering"]["vendor"], "cost": item["catering"]["total_cost"]})
            report += f"- Catering: {item['catering']['vendor']} (ID: {res['confirmation_id']})\n"
            
    return {"final_report": report, "messages": [AIMessage(content="Booking finalized.")]}

def should_approve(state: AgentState):
    if state["approval_required"]:
        return "human_approval"
    return "execute"

def create_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("planner", planner_node)
    workflow.add_node("coordinator", coordinator_node)
    workflow.add_node("budget_manager", budget_manager_node)
    workflow.add_node("human_approval", human_approval_node)
    workflow.add_node("execute", executive_node)
    
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "coordinator")
    workflow.add_edge("coordinator", "budget_manager")
    
    workflow.add_conditional_edges(
        "budget_manager",
        should_approve,
        {
            "human_approval": "human_approval",
            "execute": "execute"
        }
    )
    
    workflow.add_edge("human_approval", "execute")
    workflow.add_edge("execute", END)
    
    return workflow.compile()
