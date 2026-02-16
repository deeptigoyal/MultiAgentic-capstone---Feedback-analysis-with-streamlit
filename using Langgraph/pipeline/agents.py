import re
import csv
from typing import List
from pipeline.state import FeedbackState
from pipeline.llm import llm
from pipeline.config import logger
import pandas as pd
from pipeline.errors import DataLoadError, ModelError, OutputWriteError





# csv_reader_agent
# feedback_classifier_agent
# bug_analysis_agent
# feature_extraction_agent
# ticket_creation_agent
# quality_critic_agent

# === USER PROFILE COLLECTION ===
# PATTERN: ReAct (LLM extraction = Reason → Update profile = Action)
# MODULE: Perception + Learning (extracts missing profile info)
#async def csv_reader_agent(state: FeedbackState) -> FeedbackState:
#    return state

def csv_reader_agent(
    file_path: str,
    source_type: str
) -> List[FeedbackState]:
    """
    Reads feedback CSV and converts each row into FeedbackState.
    source_type: 'review' or 'email' 
    """
   
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise DataLoadError(f"Failed to load {file_path}: {e}")

    print(f'\nThe column names in this csv {file_path} are-->', df.columns)

    feedback_states: List[FeedbackState] = []

    for _, row in df.iterrows():
        if source_type == "review":
            raw_text = row.get("review_text", "")
            source_id = str(row.get("review_id"))
        else:  # support email
            raw_text = f"{row.get('subject', '')}. {row.get('body', '')}"
            source_id = str(row.get("email_id"))

        state: FeedbackState = {
            "input_filename": file_path,
            "source_id": source_id,
            "source_type": source_type,
            "raw_text": raw_text,

            "category": None,
            "confidence": None,
            "priority": None,

            "technical_details": None,
            "feature_details": None,

            "ticket_title": None,
            "ticket_description": None,

            "manual_review_flag": False,
            "qc_feedback": [],

            "processing_log": [
                f"CSV Reader: Loaded {source_type} record {source_id}"
            ]
        }

        feedback_states.append(state)

    logger.info(
        f"Loaded {len(feedback_states)} records from {file_path} as {source_type}"
    )
    print('\n feedback state is/are -->',feedback_states)
    return feedback_states



#async def feedback_classifier_agent(state: FeedbackState) -> FeedbackState:
#    return state

# === FEEDBACK CLASSIFIER AGENT ===
async def feedback_classifier_agent(state: FeedbackState) -> FeedbackState:
    raw_text = state.get("raw_text", "")
    metadata = state.get("metadata", {})

    print('Raw text is -->',raw_text)
    print('Metadat is--->', metadata)


    processing_log: List[str] = state.get("processing_log", [])

    # --- LLM Prompt ---
    prompt = (
        f"Classify the following user feedback into one of: "
        f"'Bug', 'Feature Request', 'Praise', 'Complaint', 'Spam'. "
        f"Provide a confidence score (0-1) and suggest an initial priority "
        f"(Critical, High, Medium, Low).\n\n"
        f"Feedback: {raw_text}\n"
        f"Metadata: {metadata}\n\n"
        f"Format: category: <category>\n"
        f"confidence: <0-1>\n"
        f"priority: <priority>\n"
    )

    # --- Call LLM ---

    try:
        response = await llm.ainvoke(prompt)
    except Exception as e:
        raise ModelError(f"LLM failure: {e}")


    message = response.content.strip()
    processing_log.append(f"Classifier prompt: {prompt}")
    processing_log.append(f"Classifier response: {message}")

    # --- Parse LLM response ---
    category_match = re.search(r"category:\s*(\w+)", message, re.IGNORECASE)
    confidence_match = re.search(r"confidence:\s*([0-1]\.?\d*)", message)
    priority_match = re.search(r"priority:\s*(\w+)", message, re.IGNORECASE)

    category = category_match.group(1) if category_match else "Unknown"
    confidence = float(confidence_match.group(1)) if confidence_match else None
    priority = priority_match.group(1) if priority_match else "Medium"

    # --- Update state ---
    state.update({
        "category": category,
        "confidence": confidence,
        "priority": priority,
        "processing_log": processing_log
    })

    return state

#async def bug_analysis_agent(state: FeedbackState) -> FeedbackState:
#    return state

async def bug_analysis_agent(state: FeedbackState) -> FeedbackState:
    if state.get("category") != "Bug":
        # Skip if not a bug
        return state

    raw_text = state.get("raw_text", "")
    metadata = state.get("metadata", {})

    print('\n Raw Data',raw_text)
    print('\n Metadata',metadata)

    processing_log: List[str] = state.get("processing_log", [])

    # --- LLM Prompt ---
    prompt = (
        f"Analyze this bug report and extract technical details:\n"
        f"- Device/OS information\n"
        f"- Steps to reproduce\n"
        f"- Severity (Critical/High/Medium/Low)\n"
        f"Provide the output in structured format.\n\n"
        f"Feedback: {raw_text}\n"
        f"Metadata: {metadata}\n"
        f"Format:\n"
        f"device_info: <device info>\n"
        f"os_version: <OS info>\n"
        f"steps_to_reproduce: <steps>\n"
        f"severity: <severity>\n"
    )

    response = await llm.ainvoke(prompt)
    message = response.content.strip()

    processing_log.append(f"Bug Analysis prompt: {prompt}")
    processing_log.append(f"Bug Analysis response: {message}")

    # --- Parse LLM response ---
    device_info_match = re.search(r"device_info:\s*(.*)", message)
    os_version_match = re.search(r"os_version:\s*(.*)", message)
    steps_match = re.search(r"steps_to_reproduce:\s*(.*)", message)
    severity_match = re.search(r"severity:\s*(.*)", message, re.IGNORECASE)

    technical_details = {
        "device_info": device_info_match.group(1) if device_info_match else "",
        "os_version": os_version_match.group(1) if os_version_match else "",
        "steps_to_reproduce": steps_match.group(1) if steps_match else "",
    }

    priority = severity_match.group(1) if severity_match else state.get("priority", "Medium")

    # --- Update state ---
    state.update({
        "technical_details": technical_details,
        "priority": priority,
        "processing_log": processing_log
    })

    return state


#async def feature_extraction_agent(state: FeedbackState) -> FeedbackState:
#    return state
async def feature_extraction_agent(state: FeedbackState) -> FeedbackState:
    if state.get("category") != "Feature Request":
        # Skip if not a feature request
        return state

    raw_text = state.get("raw_text", "")
    metadata = state.get("metadata", {})
    processing_log: List[str] = state.get("processing_log", [])

    # --- LLM Prompt ---
    prompt = (
        f"Analyze this feature request and extract actionable details:\n"
        f"- Feature description\n"
        f"- User intent / goal\n"
        f"- Estimated user impact / demand\n"
        f"Provide the output in structured format.\n\n"
        f"Feedback: {raw_text}\n"
        f"Metadata: {metadata}\n"
        f"Format:\n"
        f"feature_description: <description>\n"
        f"user_intent: <intent>\n"
        f"user_impact: <high/medium/low>\n"
    )

    # --- Call LLM ---
    response = await llm.ainvoke(prompt)
    message = response.content.strip()

    processing_log.append(f"Feature Extraction prompt: {prompt}")
    processing_log.append(f"Feature Extraction response: {message}")

    # --- Parse LLM response ---
    description_match = re.search(r"feature_description:\s*(.*)", message)
    intent_match = re.search(r"user_intent:\s*(.*)", message)
    impact_match = re.search(r"user_impact:\s*(.*)", message, re.IGNORECASE)

    feature_details = {
        "feature_description": description_match.group(1) if description_match else "",
        "user_intent": intent_match.group(1) if intent_match else "",
        "user_impact": impact_match.group(1) if impact_match else "Medium"
    }

    # --- Update state ---
    state.update({
        "feature_details": feature_details,
        "processing_log": processing_log
    })

    return state



#async def ticket_creation_agent(state: FeedbackState) -> FeedbackState:
#    return state

#ticket agent which combines outputs from Bug Analysis or Feature Extraction into structured tickets.
async def ticket_creation_agent(state: FeedbackState) -> FeedbackState:
    category = state.get("category", "")
    priority = state.get("priority", "Medium")
    technical_details = state.get("technical_details", {})
    feature_details = state.get("feature_details", {})
    processing_log: List[str] = state.get("processing_log", [])

    # --- Construct ticket ---
    if category == "Bug":
        ticket_title = f"[BUG] {technical_details.get('device_info', '')} - Issue"
        ticket_description = (
            f"Category: {category}\n"
            f"Priority: {priority}\n"
            f"Device Info: {technical_details.get('device_info', '')}\n"
            f"OS Version: {technical_details.get('os_version', '')}\n"
            f"Steps to Reproduce: {technical_details.get('steps_to_reproduce', '')}\n"
        )
    elif category == "Feature Request":
        ticket_title = f"[FEATURE REQUEST] {feature_details.get('feature_description', '')[:50]}"
        ticket_description = (
            f"Category: {category}\n"
            f"Priority: {priority}\n"
            f"Feature Description: {feature_details.get('feature_description', '')}\n"
            f"User Intent: {feature_details.get('user_intent', '')}\n"
            f"Estimated User Impact: {feature_details.get('user_impact', 'Medium')}\n"
        )
    else:
        ticket_title = f"[{category.upper()}] Feedback"
        ticket_description = f"Category: {category}\nPriority: {priority}\n"

    # Include metadata
    metadata = state.get("metadata", {})
    for key, value in metadata.items():
        ticket_description += f"{key}: {value}\n"

    processing_log.append(f"Ticket Created: {ticket_title}")

    import csv
    from typing import List
    # --- CSV Logging ---
    ticket_row = {
        "source_id": state["source_id"],
        "source_type": state["source_type"],
        "raw_text": state["raw_text"],

        "predicted_category": category,
        "confidence": state.get("confidence"),
        "priority": priority,


        "ticket_title": ticket_title,
        "ticket_description": ticket_description,
        #"category": category,
        #"priority": priority,
        "technical_details": str(technical_details),
        "feature_details": str(feature_details),
        "metadata": str(metadata)
    }

    #csv_file = f"generated_tickets_" + state["input_filename"]
    csv_file = f"generated_tickets.csv"
    fieldnames = list(ticket_row.keys())

    # Append to CSV (write header if empty)
    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if f.tell() == 0:
            writer.writeheader()
        
        try:
            writer.writerow(ticket_row)
        except Exception as e:
            raise OutputWriteError(f"Failed writing ticket CSV: {e}")


    # --- Update state ---
    state.update({
        "ticket_title": ticket_title,
        "ticket_description": ticket_description,
        "ticket_metadata": metadata,
        "processing_log": processing_log
    })

    return state




#async def quality_critic_agent(state: FeedbackState) -> FeedbackState:
#    return state

#Quality Critic Agent, which validates ticket completeness, accuracy, and flags for human review if needed.
async def quality_critic_agent(state: FeedbackState) -> FeedbackState:
    ticket_title = state.get("ticket_title", "")
    ticket_description = state.get("ticket_description", "")
    category = state.get("category", "")
    confidence = state.get("confidence", 1.0)
    processing_log: List[str] = state.get("processing_log", [])

    manual_review_flag = False
    qc_feedback = []

    # --- Basic checks ---
    if not ticket_title:
        manual_review_flag = True
        qc_feedback.append("Ticket title missing.")
    if not ticket_description:
        manual_review_flag = True
        qc_feedback.append("Ticket description missing.")
    if category in ["Bug", "Feature Request"] and confidence is not None and confidence < 0.7:
        manual_review_flag = True
        qc_feedback.append(f"Low confidence ({confidence}) for category {category}.")

    if manual_review_flag:
        processing_log.append(f"Quality Critic flagged manual review: {qc_feedback}")
    else:
        processing_log.append("Quality Critic passed: ticket looks complete.")

    # --- Update state ---
    state.update({
        "manual_review_flag": manual_review_flag,
        "qc_feedback": qc_feedback,
        "processing_log": processing_log
    })

    return state

async def end_node(state: FeedbackState) -> FeedbackState:
    return state

