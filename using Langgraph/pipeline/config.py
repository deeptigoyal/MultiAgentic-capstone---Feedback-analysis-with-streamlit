import os
import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

logger = logging.getLogger("feedback_pipeline")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = RotatingFileHandler(
        "outputs/feedback_pipeline.log",
        maxBytes=5_000_000,
        backupCount=3
    )
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
