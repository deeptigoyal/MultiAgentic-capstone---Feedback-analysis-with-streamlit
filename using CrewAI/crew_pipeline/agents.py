from crewai import Agent
from .llm import get_llm

def feedback_classifier_agent():
    return Agent(
        role="Feedback Classifier",
        goal="Classify user feedback accurately",
        backstory="Expert at understanding customer feedback",
        llm=get_llm(),
        verbose=True
    )


#Bug analsis agent
bug_analysis_agent = Agent(
    role="Bug Analyst",
    goal="Extract technical details from bug reports",
    backstory="Expert in analyzing software bugs and extracting reproducible technical details.",
    llm=get_llm(),
    verbose=True
)

#Feature Extractor Agent
feature_extraction_agent = Agent(
    role="Feature Analyst",
    goal="Extract structured feature request details from user feedback",
    backstory=(
        "You analyze feature requests and convert them into clear, "
        "actionable product requirements."
    ),
    llm=get_llm(),
    verbose=True
)

#Ticket Creator Agent
ticket_creator_agent = Agent(
    role="Ticket Creator",
    goal="Create structured tickets from analyzed feedback",
    backstory=(
        "You convert classified and analyzed feedback into clear, "
        "actionable tickets with proper priority and metadata."
    ),
    llm=get_llm(),
    verbose=True
)


# if __name__ == "__main__":
#     agent = feedback_classifier_agent()
#     print(agent.role)
