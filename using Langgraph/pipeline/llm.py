from langchain_groq import ChatGroq
from pipeline.config import GROQ_API_KEY
import os

llm = ChatGroq(
    groq_api_key= os.getenv(GROQ_API_KEY),
    model_name= "llama-3.1-8b-instant"
)
