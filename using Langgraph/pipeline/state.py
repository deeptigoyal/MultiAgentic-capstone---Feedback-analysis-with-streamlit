from typing import TypedDict, Optional, Dict, List

class FeedbackState(TypedDict):
    source_id: str
    source_type: str
    raw_text: str
    metadata: Dict[str, str]

    category: Optional[str]
    confidence: Optional[float]
    priority: Optional[str]

    technical_details: Optional[str]
    feature_details: Optional[str]

    ticket_title: Optional[str]
    ticket_description: Optional[str]
    ticket_metadata: Optional[Dict[str, str]]

    qc_status: Optional[str]
    qc_feedback: Optional[str]

    manual_review_flag: Optional[bool]
    processing_log: Optional[List[str]]
