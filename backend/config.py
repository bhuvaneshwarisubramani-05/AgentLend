# backend/config.py
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env file

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set! Please add it to your .env file.")
