
from crewai import Crew
from .agents import (
    feedback_classifier_agent,
    bug_analysis_agent,
    feature_extraction_agent,
    ticket_creator_agent
)
from .tasks import (
    classify_feedback_task,
    bug_analysis_task,
    feature_extraction_task,
    ticket_creation_task
)


def run_full_pipeline(feedback_text: str, source: str = "app_review"):
    """
    End-to-end feedback pipeline:
    Classification → (Bug OR Feature Analysis) → Ticket Creation
    """

    # -------- Agents --------
    classifier = feedback_classifier_agent()
    bug_agent = bug_analysis_agent
    feature_agent = feature_extraction_agent
    ticket_agent = ticket_creator_agent

    # -------- Step 1: Classification --------
    classify_task = classify_feedback_task(classifier, feedback_text)

    # -------- Step 2: Conditional tasks --------
    # NOTE: CrewAI cannot branch dynamically yet.
    # We run both and let the LLM output decide relevance.
    bug_task = bug_analysis_task(bug_agent, feedback_text)
    feature_task = feature_extraction_task(feature_agent, feedback_text)

    # -------- Step 3: Ticket creation --------
    ticket_task = ticket_creation_task(ticket_agent)

    crew = Crew(
        agents=[classifier, bug_agent, feature_agent, ticket_agent],
        tasks=[
            classify_task,
            bug_task,
            feature_task,
            ticket_task
        ],
        verbose=True
    )

    result = crew.kickoff()

    print("\n===== CREW OUTPUT =====")
    print(result)
    print("=======================\n")

    return result

# # ------------------------------
# # Independent test run
# # ------------------------------
# if __name__ == "__main__":
#     output = run_full_pipeline(
#         "Please add dark mode and calendar sync",
#         source="support_email"
#     )
#     print(output)
