"""Week 5 Day 1 - AutoGen HR Assistant Agent.

An AssistantAgent with the system message "You are an HR assistant."
that writes a 5-line job description for any role.
"""

import asyncio
import os
import sys

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()


def build_task(role: str) -> str:
    # Say exactly what "5 lines" means, so the model cannot guess.
    return (
        f"Write a job description for a {role}. "
        "Reply with exactly 5 numbered lines (1. to 5.), each one short sentence "
        "covering: responsibilities, required skills, tools, teamwork and growth. "
        "No title, no introduction, no closing remarks, nothing else."
    )


async def main() -> None:
    # API key comes from the OPENAI_API_KEY environment variable, never hard-coded.
    if not os.getenv("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY is not set. Add it to .env and run again.")

    role = input("Which role? (press Enter for Junior Python Developer): ").strip()
    role = role or "Junior Python Developer"

    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

    agent = AssistantAgent(
        name="hr_assistant",
        model_client=model_client,
        system_message="You are an HR assistant.",
    )

    try:
        await Console(agent.run_stream(task=build_task(role)))
    finally:
        # An unclosed client leaves the script hanging.
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
