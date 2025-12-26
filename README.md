# Feedback-analysis-with-langraph-streamlit


Multi-Agent Feedback AI System

This project implements a modular, multi-agent AI pipeline to automatically process user feedback and generate structured engineering tickets. The codebase is organized for clarity, scalability, and separation of concerns.

The app.py file contains only the Streamlit user interface, enabling CSV upload, pipeline execution, monitoring, and ticket download without embedding business logic.

All core logic resides in the pipeline/ package. state.py defines the shared FeedbackState, ensuring consistent data flow across agents. config.py manages environment variables, API keys, and logging setup, while llm.py initializes the ChatGroq model used by agents. agents.py contains specialized agents for classification, bug analysis, feature extraction, ticket creation, and quality control. graph.py builds the LangGraph workflow with conditional routing, and runner.py orchestrates end-to-end execution for each feedback record.

The data/ directory stores mock input datasets and ground truth for evaluation. Generated outputs, including tickets and logs, are written to outputs/. Dependencies and environment configuration are managed via requirements.txt and .env.


- With Langgraph

feedback_ai/
│
├── app.py
│
├── pipeline/
│   ├── __init__.py
│   ├── state.py
│   ├── config.py
│   ├── llm.py
│   ├── agents.py
│   ├── graph.py
│   ├── runner.py
│
├── data/
│   ├── app_store_reviews.csv
│   ├── support_emails.csv
│   └── expected_classifications.csv
│
├── outputs/
│   ├── generated_tickets.csv
│   └── feedback_pipeline.log
│
├── requirements.txt
└── .env



- With CrewAI

feedback_ai_crewai/
│
├── app.py                       # (Optional) Streamlit UI
│
├── crew/
│   ├── __init__.py
│   ├── llm.py                   # LLM config (Groq/OpenAI)
│   ├── agents.py                # CrewAI Agents
│   ├── tasks.py                 # Tasks mapped to agents
│   ├── crew.py                  # Crew definition & execution
│
├── tools/
│   ├── csv_reader.py
│   ├── ticket_writer.py
│
├── data/
│   ├── app_store_reviews.csv
│   ├── support_emails.csv
│
├── outputs/
│   ├── generated_tickets.csv
│   ├── processing_log.csv
│   └── metrics.csv
│
├── requirements.txt
└── .env

- Differece in Langgraph and CrewAI mapping. What Changes Fundamentally in CrewAI?

1. No StateGraph → CrewAI manages flow via tasks

2. No async graph orchestration → CrewAI is mostly sequential

3. State becomes task outputs, not a TypedDict

4. Memory optional, not structural

5. Much simpler mental model for demos and MVPs
![Uploading Screenshot 2025-12-26 at 7.34.29 PM.png…]()

  

<img width="423" height="383" alt="Screenshot 2025-12-26 at 7 34 29 PM" src="https://github.com/user-attachments/assets/e32b6c4e-6bfd-441f-a6a1-628eefba1307" />

