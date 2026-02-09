import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

MODEL_NAME = "llama-3.1-8b-instant"
MAX_TURNS = 2

if not GROQ_API_KEY:
    raise RuntimeError("Missing GROQ_API_KEY in .env")
if not TAVILY_API_KEY:
    raise RuntimeError("Missing TAVILY_API_KEY in .env")
