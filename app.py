import gradio as gr

from researchmanager import ResearchManager


async def run(query: str):

    if not query.strip():
        yield "⚠️ Please enter a research question."
        return

    async for status_update in ResearchManager().run(query):
        yield status_update


with gr.Blocks(
    title="Deep Research"
) as ui:

    gr.Markdown(
        """
        # 🔎 Deep Research

        Ask a question and let the AI research it
        and generate a detailed report.
        """
    )

    with gr.Row():

        query_textbox = gr.Textbox(
            placeholder="Type a research question...",
            show_label=False,
            lines=2,
            scale=5
        )

        run_button = gr.Button(
            "Investigate",
            variant="primary",
            scale=1
        )

    gr.Markdown("### Try one")

    gr.Examples(
        examples=[
            ["Most popular AI Agent frameworks in 2026"],
            ["What are the best Python frameworks for AI Agents?"],
            ["What are the latest trends in Generative AI?"],
            ["How is RAG evolving in 2026?"]
        ],
        inputs=query_textbox
    )

    report = gr.Markdown(
        value="Your research report will appear here..."
    )

    run_button.click(
        fn=run,
        inputs=query_textbox,
        outputs=report
    )

    query_textbox.submit(
        fn=run,
        inputs=query_textbox,
        outputs=report
    )


if __name__ == "__main__":
    ui.launch()