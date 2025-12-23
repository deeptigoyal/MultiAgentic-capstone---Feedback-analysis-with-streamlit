# Feedback-analysis-with-streamlit


Multi-Agent Feedback AI System

This project implements a modular, multi-agent AI pipeline to automatically process user feedback and generate structured engineering tickets. The codebase is organized for clarity, scalability, and separation of concerns.

The app.py file contains only the Streamlit user interface, enabling CSV upload, pipeline execution, monitoring, and ticket download without embedding business logic.

All core logic resides in the pipeline/ package. state.py defines the shared FeedbackState, ensuring consistent data flow across agents. config.py manages environment variables, API keys, and logging setup, while llm.py initializes the ChatGroq model used by agents. agents.py contains specialized agents for classification, bug analysis, feature extraction, ticket creation, and quality control. graph.py builds the LangGraph workflow with conditional routing, and runner.py orchestrates end-to-end execution for each feedback record.

The data/ directory stores mock input datasets and ground truth for evaluation. Generated outputs, including tickets and logs, are written to outputs/. Dependencies and environment configuration are managed via requirements.txt and .env.
