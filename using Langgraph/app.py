
#on temrinal write: export PATH="/Users/deeptigoel/anaconda3/envs/capstone_py310/bin:$PATH"

import streamlit as st
import pandas as pd
import asyncio
import tempfile
import os
from pipeline.runner import run_pipeline

# import EVERYTHING from your existing file
# from feedback_pipeline import run_pipeline

st.set_page_config(page_title="Multi-Agent Feedback Pipeline", layout="wide")

st.title("📩 Multi-Agent Feedback Processing System using Langgraph")

st.markdown("""
This app:
- Reads feedback CSVs (App Reviews / Support Emails)
- Classifies feedback
- Extracts technical insights
- Generates structured tickets
- Uses ChatGroq as llm
""")

# ---- File Upload ----
uploaded_file = st.file_uploader(
    "Upload feedback CSV",
    type=["csv"]
)

source_type = st.selectbox(
    "Select feedback source type",
    ["review", "email"]
)

run_btn = st.button("🚀 Run Pipeline")

# ---- Run Pipeline ----
if run_btn and uploaded_file:

    with st.spinner("Processing feedback through multi-agent pipeline..."):

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            tmp.write(uploaded_file.getbuffer())
            tmp_path = tmp.name

        try:
            results = asyncio.run(
                run_pipeline(
                    csv_path=tmp_path,
                    source_type=source_type
                )
            )

            # Convert results to DataFrame
            rows = []
            for r in results:
                rows.append({
                    "source_id": r["source_id"],
                    "category": r["category"],
                    "confidence": r["confidence"],
                    "priority": r["priority"],
                    "ticket_title": r["ticket_title"],
                    "manual_review": r["manual_review_flag"]
                })

            df_out = pd.DataFrame(rows)

            st.success("✅ Processing completed")

            st.subheader("📊 Results Preview")
            st.dataframe(df_out, use_container_width=True)

            # ---- Download ----
            csv_data = df_out.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download Tickets CSV",
                csv_data,
                file_name="generated_tickets.csv",
                mime="text/csv"
            )

        finally:
            os.remove(tmp_path)
