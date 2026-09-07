import os
import json
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic import BaseModel, Field

load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

openrouter_client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_api_key
)


class WebSearchItem(BaseModel):
    reason: str = Field(
        description="Why this search is important for answering the query."
    )

    query: str = Field(
        description="The search query to perform."
    )


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(
        description="The list of web searches needed to answer the query."
    )


HOW_MANY_SEARCHES = 3


INSTRUCTIONS = f"""
You are a research assistant.

Given a user's query, create a plan for web research.

You must create exactly {HOW_MANY_SEARCHES} searches.

For each search:
1. Explain briefly why the search is important.
2. Provide a clear and useful search query.

Return ONLY valid JSON.

The JSON must have exactly this structure:

{{
    "searches": [
        {{
            "reason": "Why this search is important",
            "query": "The search query"
        }},
        {{
            "reason": "Why this search is important",
            "query": "The search query"
        }},
        {{
            "reason": "Why this search is important",
            "query": "The search query"
        }}
    ]
}}

Do not write anything before or after the JSON.
"""


async def create_search_plan(query: str) -> WebSearchPlan:

    response = await openrouter_client.chat.completions.create(
        model="minimax/minimax-m2.7:free",

        messages=[
            {
                "role": "system",
                "content": INSTRUCTIONS
            },
            {
                "role": "user",
                "content": query
            }
        ],

        response_format={
            "type": "json_object"
        }
    )

    content = response.choices[0].message.content

    print("\n========== RAW MODEL OUTPUT ==========\n")
    print(content)

    try:
        data = json.loads(content)

        plan = WebSearchPlan.model_validate(data)

        return plan

    except Exception as e:
        print("\nError while parsing WebSearchPlan:")
        print(e)
        raise