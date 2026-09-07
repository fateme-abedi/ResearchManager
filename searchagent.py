import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI

from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    ModelSettings,
    set_tracing_disabled,
)
from agents import function_tool
from ddgs import DDGS
load_dotenv()
openrouter_api_key=os.getenv("OPENROUTER_API_KEY")
set_tracing_disabled(True)

openrouter_client=AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_api_key,
)

minimax_model=OpenAIChatCompletionsModel(
     model="minimax/minimax-m2.7:free",
     openai_client=openrouter_client
)

@function_tool
def search_web(query: str) -> str:
    """
    Search the web for the given query and return the search results.

    Args:
        query: The search query to search for.
    """

    results = DDGS().text(
        query,
        max_results=5
    )

    if not results:
        return "No search results found."

    output = []

    for result in results:
        title = result.get("title", "")
        url = result.get("href", "")
        snippet = result.get("body", "")

        output.append(
            f"Title: {title}\n"
            f"URL: {url}\n"
            f"Summary: {snippet}"
        )

    return "\n\n".join(output)


search_agent=Agent(
    name="search_agent",
    instructions="""
    You are a research assistant.

    When the user asks for current information,
    use the web_search tool.

    After receiving the search results,
    summarize them in 2-3 paragraphs.
    """,
    tools=[search_web],
    model=minimax_model,
    model_settings=ModelSettings(
        tool_choice="auto"
    )
)

async def main():
    task = "Most popular AI Agent frameworks in 2026"
    result=await Runner.run(
        search_agent,
        task
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())