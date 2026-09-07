import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic import BaseModel, Field

from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    ModelSettings,
    set_tracing_disabled,
)

load_dotenv()
openrouter_api_key=os.getenv("OPENROUTER_API_KEY")
set_tracing_disabled(True)


openrouter_client=AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_api_key
)

minimax_model=OpenAIChatCompletionsModel(
    model="minimax/minimax-m2.7:free",
    openai_client=openrouter_client
)

INSTRUCTIONS = """
You are a senior researcher tasked with writing a cohesive report for a research query.
You will be provided with the original query, and some research.
Generate a comprehensive report based on the research and the query.
The final output should be in markdown format, and it should be lengthy and detailed. Aim 
for 5-10 pages of content, at least 1000 words.
"""


class ReportData(BaseModel):
    short_summary: str = Field(description="A short 2-3 sentence summary of the findings.")
    markdown_report: str = Field(description="The final report")
    follow_up_questions: list[str] = Field(description="Suggested topics to research further")


writer_agent = Agent(
    name="Writer Agent",
     instructions=INSTRUCTIONS, 
     model=minimax_model, 
     )


async def main():

    task = """
    Original Query:
    What are the most popular AI Agent frameworks in 2026?

    Research:
    
    LangChain is a popular framework for building applications
    powered by large language models and AI agents.

    CrewAI focuses on orchestrating multiple AI agents that work
    together to accomplish complex tasks.

    Microsoft AutoGen is designed for multi-agent conversations
    and agent collaboration.

    OpenAI Agents SDK provides tools for building agentic
    applications with agents, tools, handoffs, and guardrails.
    """

    result = await Runner.run(
        writer_agent,
        task
    )

    print("\n========== WRITER OUTPUT ==========\n")

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())