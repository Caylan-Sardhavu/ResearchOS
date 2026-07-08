from dotenv import load_dotenv
import os

load_dotenv()

FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")
MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "accounts/fireworks/models/llama-v3p1-8b-instruct"
)