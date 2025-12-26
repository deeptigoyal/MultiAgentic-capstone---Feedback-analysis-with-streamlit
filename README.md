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

<img width="353" height="456" alt="Screenshot 2025-12-26 at 7 20 45 PM" src="https://github.com/user-attachments/assets/959b5fc9-3fc0-4c49-a347-73277647f498" />






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

<img width="455" height="485" alt="Screenshot 2025-12-26 at 7 29 12 PM" src="https://github.com/user-attachments/assets/8bba7584-2f2d-4935-aca5-73fa7adbf5d7" />
