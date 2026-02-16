import streamlit as st
import pandas as pd
import sys
import os

# Load environment variables (.env → OPENAI_API_KEY)
from dotenv import load_dotenv
load_dotenv()

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from crew_pipeline.crew_feedback import run_full_pipeline
from tools.ticket_writer import write_ticket_to_csv

st.set_page_config(page_title="Feedback AI Pipeline", layout="wide")
st.title("📩 Feedback AI – CrewAI Pipeline")


import re

# Helper function to extract fields from CrewAI output
def parse_pipeline_output(output_str):
    """
    Expects output_str to contain:
    Ticket Title, Ticket Description, Priority, Category, Confidence
    """
    result = {
        "ticket_title": "",
        "ticket_description": "",
        "priority": "",
        "category": "",
        "confidence": ""
    }

    # Use regex to capture each field
    patterns = {
        "ticket_title": r"Ticket Title\s*:\s*(.*)",
        "ticket_description": r"Ticket Description\s*:\s*(.*)",
        "priority": r"Priority\s*:\s*(.*)",
        "category": r"Category\s*:\s*(.*)",
        "confidence": r"Confidence\s*:\s*(.*)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, output_str, re.IGNORECASE)
        if match:
            result[key] = match.group(1).strip().replace('**','')

    return result

# Step 1: User selects feedback type
feedback_type = st.selectbox(
    "Select feedback type",
    ["app_review", "email"],
    format_func=lambda x: "App Review" if x == "app_review" else "Email"
)

uploaded_file = st.file_uploader("Upload feedback CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Uploaded Data")
    st.dataframe(df)

    # Step 2: Determine which column to use
    column_map = {
        "app_review": "review_text",
        "email": "body"
    }
    selected_column = column_map[feedback_type]

    # ✅ SAFETY CHECK: ensure required column exists
    if selected_column not in df.columns:
        st.error(f"CSV must contain a `{selected_column}` column for {feedback_type.replace('_', ' ')}")
        st.stop()

    # ✅ SAFETY CHECK: ensure ID column exists
    id_column_map = {
        "app_review": "review_id",
        "email": "email_id"
    }
    source_column = id_column_map[feedback_type]
    if source_column not in df.columns:
        st.error(f"CSV must contain a `{source_column}` column for {feedback_type.replace('_', ' ')}")
        st.stop()

    if st.button("🚀 Run Pipeline"):
        results = []

        #for idx, row in df.head(2).iterrows():
        for idx, row in df.iterrows():
            feedback_text = str(row[selected_column])
            source = row[source_column]  # <-- dynamic based on feedback type

            st.write(f"🔍 Processing row {idx + 1}")

            # ---- Run full CrewAI pipeline ----
            output = run_full_pipeline(
                feedback_text=feedback_text,
                source=source
            )

            # ---- Normalize output (Crew returns string/dict) ----
            parsed_output = parse_pipeline_output(str(output))

            # ---- Normalize output (Crew returns string/dict) ----
            ticket = {
                "source_id": source,
                "input_text": feedback_text,
                "pipeline_output": str(output),  # ✅ force safe serialization
                "ticket_title": parsed_output["ticket_title"],
                "ticket_description": parsed_output["ticket_description"],
                "priority": parsed_output["priority"],
                "category": parsed_output["category"],
                "confidence": parsed_output["confidence"]
            }

            write_ticket_to_csv(ticket, feedback_type)
            results.append(ticket)

        result_df = pd.DataFrame(results)

        st.success("✅ Pipeline completed!")
        st.subheader("🎫 Generated Tickets")
        st.dataframe(result_df, use_container_width=True)

        st.download_button(
            "⬇️ Download Tickets CSV",
            data=result_df.to_csv(index=False),
            file_name="generated_tickets"+feedback_type+".csv",
            mime="text/csv"
        )
