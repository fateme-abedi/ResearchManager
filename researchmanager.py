import asyncio

from agents import Runner

from planneragent import create_search_plan
from searchagent import search_agent
from writeragent import writer_agent


async def search(item):

    input_message = (
        f"Search term: {item.query}\n"
        f"Reason for searching: {item.reason}"
    )

    result = await Runner.run(
        search_agent,
        input_message
    )

    return result.final_output


class ResearchManager:

    async def run(self, query: str):

        # =========================
        # 1. Planning
        # =========================

        yield "🧠 Planning the research..."

        plan = await create_search_plan(query)

        yield (
            f"📋 Planner created "
            f"{len(plan.searches)} search queries."
        )

        # =========================
        # 2. Display search queries
        # =========================

        for i, item in enumerate(
            plan.searches,
            start=1
        ):

            yield (
                f"🔎 Search {i}: {item.query}\n\n"
                f"Reason: {item.reason}"
            )

        # =========================
        # 3. Web Search
        # =========================

        yield "🌐 Searching the web..."

        tasks = [
            search(item)
            for item in plan.searches
        ]

        search_results = await asyncio.gather(
            *tasks
        )

        yield "✅ All web searches completed."

        # =========================
        # 4. Writer
        # =========================

        yield "✍️ Writing the final report..."

        input_message = (
            f"Original query:\n"
            f"{query}\n\n"
            f"Research results:\n"
            f"{search_results}"
        )

        result = await Runner.run(
            writer_agent,
            input_message
        )

        # =========================
        # 5. Final Report
        # =========================

        yield result.final_output