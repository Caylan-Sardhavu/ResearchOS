from fireworks.client import Fireworks

from app.core.settings import (
    FIREWORKS_API_KEY,
    MODEL_NAME,
)


class FireworksService:

    def __init__(self):
        self.client = None

        if FIREWORKS_API_KEY:
            self.client = Fireworks(api_key=FIREWORKS_API_KEY)

    def available(self):
        return self.client is not None

    def chat(self, prompt: str):

        if not self.client:
            return {
                "success": False,
                "message": "Fireworks API key not configured."
            }

        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return {
            "success": True,
            "response": response.choices[0].message.content
        }