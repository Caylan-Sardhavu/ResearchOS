import os

from dotenv import load_dotenv

# Load variables from apps/backend/.env.
load_dotenv()


# Fireworks API credentials.
FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY", "").strip()

# Support both the new FIREWORKS_MODEL name and the older MODEL_NAME name.
FIREWORKS_MODEL = os.getenv(
    "FIREWORKS_MODEL",
    os.getenv(
        "MODEL_NAME",
        "accounts/fireworks/models/llama-v3p1-8b-instruct",
    ),
).strip()

# Allows Fireworks to be disabled without removing the API key.
USE_FIREWORKS = os.getenv("USE_FIREWORKS", "false").lower() in {
    "1",
    "true",
    "yes",
    "on",
}

# Fireworks exposes an OpenAI-compatible API at this base URL.
FIREWORKS_BASE_URL = os.getenv(
    "FIREWORKS_BASE_URL",
    "https://api.fireworks.ai/inference/v1",
).strip()

# Conservative defaults to control latency and credit usage.
FIREWORKS_TIMEOUT_SECONDS = float(
    os.getenv("FIREWORKS_TIMEOUT_SECONDS", "60")
)

FIREWORKS_MAX_TOKENS = int(
    os.getenv("FIREWORKS_MAX_TOKENS", "800")
)

FIREWORKS_TEMPERATURE = float(
    os.getenv("FIREWORKS_TEMPERATURE", "0.2")
)