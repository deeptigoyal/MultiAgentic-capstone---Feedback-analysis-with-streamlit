from crewai import Task
from .agents import (
    bug_analysis_agent,
    feature_extraction_agent, 
    ticket_creator_agent
)

#Classify Task
def classify_feedback_task(agent, feedback_text):
    return Task(
        description=f"""
        Classify the feedback below into:
        Bug, Feature Request, Praise, Complaint, or Spam.
        Also suggest priority (Critical/High/Medium/Low).
        Provide a confidence score (0.0 - 1.0)


        Feedback:
        {feedback_text}
        """,
        expected_output="Category, Priority, Confidence",
        agent=agent
    )

#Bug Analysis Task
def bug_analysis_task(bug_agent, feedback_text: str):
    return Task(
        description=f"""
Analyze the following bug report and extract:
- Device info
- OS version
- Steps to reproduce
- Severity

Feedback:
{feedback_text}
""",
        expected_output="Structured technical bug details",
        agent=bug_agent
    )

#Feature Analysis Task
def feature_extraction_task(agent, classified_text):
    return Task(
        description=(
            f"Extract feature details from the following feedback:\n\n"
            f"{classified_text}\n\n"
            "Provide:\n"
            "- feature_description\n"
            "- user_intent\n"
            "- user_impact (High/Medium/Low)"
        ),
        agent=agent,
        expected_output=(
            "A structured feature summary with description, intent, and impact."
        )
    )

def ticket_creation_task(ticket_creator_agent):
    return Task(
    description=(
        "Using the feedback category, priority, technical or feature details, "
        "generate a structured ticket with:\n"
        "- Ticket Title\n"
        "- Ticket Description\n"
        "- Priority\n"
        "- Category"
        "- Confidence"
    ),
    expected_output=(
        "A structured ticket with title, description, priority, category and confidence."
    ),
    agent=ticket_creator_agent
)




if __name__ == "__main__":
    print("Task factory ready")

