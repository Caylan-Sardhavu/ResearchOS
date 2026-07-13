import asyncio

from app.services.fireworks import FireworksService


async def main() -> None:
    """
    Sends one small Fireworks request to verify the integration.
    """

    fireworks = FireworksService()

    print("Fireworks available:", fireworks.available())

    result = await fireworks.chat(
        prompt=(
            "In two short sentences, explain why memory bandwidth "
            "matters for large language model inference."
        ),
        system_prompt=(
            "You are a concise technical research assistant."
        ),
        max_tokens=120,
        temperature=0.1,
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())