from langgraph.graph import StateGraph
from pipeline.state import FeedbackState
from langgraph.checkpoint.memory import MemorySaver

from pipeline.agents import (
    feedback_classifier_agent,
    bug_analysis_agent,
    feature_extraction_agent,
    ticket_creation_agent,
    quality_critic_agent
)

def get_next_node(state: FeedbackState) -> str:
    if state.get("manual_review_flag"):
        return "End"

    category = state.get("category")
    if category == "Bug":
        return "Bug Analysis"
    elif category == "Feature Request":
        return "Feature Extraction"
    elif category in ["Praise", "Complaint"]:
        return "Ticket Creation"
    return "End"


def build_graph():
    builder = StateGraph(FeedbackState)

    builder.add_node("Feedback Classifier", feedback_classifier_agent)
    builder.add_node("Bug Analysis", bug_analysis_agent)
    builder.add_node("Feature Extraction", feature_extraction_agent)
    builder.add_node("Ticket Creation", ticket_creation_agent)
    builder.add_node("Quality Critic", quality_critic_agent)
    builder.add_node("End", lambda x: x)

    builder.set_entry_point("Feedback Classifier")

    builder.add_conditional_edges(
        "Feedback Classifier",
        get_next_node,
        {
            "Bug Analysis": "Bug Analysis",
            "Feature Extraction": "Feature Extraction",
            "Ticket Creation": "Ticket Creation",
            "End": "End"
        }
    )

    builder.add_edge("Bug Analysis", "Ticket Creation")
    builder.add_edge("Feature Extraction", "Ticket Creation")
    builder.add_edge("Ticket Creation", "Quality Critic")
    builder.add_edge("Quality Critic", "End")

    #added checkpoint for conversational memory #not needed conversational memory as such
    #checkpointer = MemorySaver()
    #return builder.compile(checkpointer=checkpointer)
    return builder.compile()
    
