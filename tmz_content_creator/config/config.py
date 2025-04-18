from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = "gpt-3.5-turbo"
    SYSTEM_PROMPT = "You are a helpful and creative AI assistant." 