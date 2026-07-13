from typing import Any

from openai import APIConnectionError
from openai import APIStatusError
from openai import APITimeoutError
from openai import AsyncOpenAI

from app.core.settings import (
    FIREWORKS_API_KEY,
    FIREWORKS_BASE_URL,
    FIREWORKS_MAX_TOKENS,
    FIREWORKS_MODEL,
    FIREWORKS_TEMPERATURE,
    FIREWORKS_TIMEOUT_SECONDS,
    USE_FIREWORKS,
)


class FireworksService:
    """
    Lightweight asynchronous client for Fireworks AI.

    All Fireworks calls return a consistent dictionary so the rest of
    ResearchOS can safely use deterministic fallback logic whenever the
    external model is unavailable or returns an invalid response.
    """

    def __init__(self) -> None:
        self.client: AsyncOpenAI | None = None

        if USE_FIREWORKS and FIREWORKS_API_KEY:
            self.client = AsyncOpenAI(
                api_key=FIREWORKS_API_KEY,
                base_url=FIREWORKS_BASE_URL,
                timeout=FIREWORKS_TIMEOUT_SECONDS,
            )

    def available(self) -> bool:
        """
        Returns True when Fireworks is enabled and configured.
        """

        return self.client is not None

    async def chat(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> dict[str, Any]:
        """
        Sends one chat-completion request to Fireworks.

        API failures are returned as structured data rather than raised
        into the ResearchOS workflow.
        """

        if not self.client:
            return {
                "success": False,
                "response": None,
                "message": (
                    "Fireworks is disabled or FIREWORKS_API_KEY "
                    "is not configured."
                ),
                "finish_reason": None,
            }

        if not prompt.strip():
            return {
                "success": False,
                "response": None,
                "message": "The Fireworks prompt cannot be empty.",
                "finish_reason": None,
            }

        messages: list[dict[str, str]] = []

        if system_prompt and system_prompt.strip():
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt.strip(),
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt.strip(),
            }
        )

        try:
            completion = await self.client.chat.completions.create(
                model=FIREWORKS_MODEL,
                messages=messages,
                max_tokens=(
                    FIREWORKS_MAX_TOKENS
                    if max_tokens is None
                    else max_tokens
                ),
                temperature=(
                    FIREWORKS_TEMPERATURE
                    if temperature is None
                    else temperature
                ),
            )

            if not completion.choices:
                return {
                    "success": False,
                    "response": None,
                    "message": "Fireworks returned no completion choices.",
                    "finish_reason": None,
                }

            choice = completion.choices[0]
            content = choice.message.content
            finish_reason = choice.finish_reason

            if not isinstance(content, str) or not content.strip():
                return {
                    "success": False,
                    "response": None,
                    "message": "Fireworks returned an empty response.",
                    "finish_reason": finish_reason,
                }

            usage = completion.usage

            return {
                "success": True,
                "response": content.strip(),
                "message": None,
                "model": FIREWORKS_MODEL,
                "finish_reason": finish_reason,
                "usage": {
                    "prompt_tokens": (
                        usage.prompt_tokens if usage else None
                    ),
                    "completion_tokens": (
                        usage.completion_tokens if usage else None
                    ),
                    "total_tokens": (
                        usage.total_tokens if usage else None
                    ),
                },
            }

        except APITimeoutError:
            return {
                "success": False,
                "response": None,
                "message": "The Fireworks request timed out.",
                "finish_reason": None,
            }

        except APIConnectionError:
            return {
                "success": False,
                "response": None,
                "message": (
                    "Unable to connect to Fireworks. Check the network, "
                    "base URL, and API availability."
                ),
                "finish_reason": None,
            }

        except APIStatusError as exc:
            try:
                error_body = exc.response.text
            except Exception:
                error_body = "No response body was available."

            try:
                request_url = str(exc.request.url)
            except Exception:
                request_url = "Unknown request URL"

            return {
                "success": False,
                "response": None,
                "message": f"Fireworks returned HTTP {exc.status_code}.",
                "finish_reason": None,
                "request_url": request_url,
                "error_body": error_body,
            }

        except Exception as exc:
            return {
                "success": False,
                "response": None,
                "message": (
                    "Unexpected Fireworks error: "
                    f"{type(exc).__name__}: {exc}"
                ),
                "finish_reason": None,
            }