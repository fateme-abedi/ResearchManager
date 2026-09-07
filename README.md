# 🔎 Deep Research AI Agent

An AI-powered **Deep Research Assistant** built with Python, the **OpenAI Agents SDK**, **OpenRouter**, and **Gradio**.

The system takes a research question, automatically creates a search plan, performs multiple web searches in parallel, and finally uses an AI agent to synthesize the collected information into a research report.

The project demonstrates how multiple AI agents can be orchestrated together to build a practical **Agentic AI research workflow**.

---

## ✨ Features

* 🤖 **AI-powered research planning**
* 🔎 Automatically generates multiple search queries
* 🌐 Performs real web searches using DuckDuckGo
* ⚡ Executes multiple searches concurrently using `asyncio`
* 🧠 Uses multiple AI agents for different responsibilities
* 📝 Automatically generates a final research report
* 📊 Structured output using **Pydantic**
* 🎨 Simple and interactive **Gradio** interface
* 🆓 Designed to work with free AI model providers
* 🔐 API keys are stored securely using environment variables

---

## 🏗️ Architecture

The project follows a multi-agent research pipeline:

```text
                    User Question
                          │
                          ▼
                 ┌─────────────────┐
                 │  ResearchManager │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │  Planner Agent  │
                 │                 │
                 │ Creates Search  │
                 │     Plan        │
                 └────────┬────────┘
                          │
                 WebSearchPlan
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
        Search #1    Search #2    Search #3
             │            │            │
             └────────────┼────────────┘
                          │
                    asyncio.gather()
                          │
                          ▼
                 ┌─────────────────┐
                 │   Search Agent  │
                 │                 │
                 │  DuckDuckGo Web │
                 │     Search      │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │  Writer Agent   │
                 │                 │
                 │ Synthesizes the │
                 │ research results│
                 └────────┬────────┘
                          │
                          ▼
                   Final Report
                          │
                          ▼
                 ┌─────────────────┐
                 │   Gradio UI     │
                 └─────────────────┘
```

---

## 🧩 Project Structure

```text
deep-research-agent/
│
├── app.py
├── planneragent.py
├── searchagent.py
├── writeragent.py
├── researchmanager.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

### `app.py`

Provides the graphical user interface using **Gradio**.

The user enters a research question and receives the generated research report.

---

### `planneragent.py`

Responsible for creating the research plan.

Given a user question, the planner generates multiple search queries.

The search plan is represented using Pydantic models:

```python
class WebSearchItem(BaseModel):
    reason: str
    query: str


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem]
```

For example:

```text
User Question:
"Most popular AI Agent frameworks in 2026"

        ↓

Search Plan:

1. AI Agent frameworks 2026
2. Most popular AI Agent frameworks
3. AI Agent framework comparison 2026
```

---

### `searchagent.py`

Responsible for performing web research.

The project uses a custom function tool based on DuckDuckGo:

```python
@function_tool
def search_web(query: str) -> str:
    ...
```

The search results are then passed to the Search Agent for processing.

---

### `writeragent.py`

The Writer Agent receives the original research question and the collected search results.

It then synthesizes the information into a coherent final report.

---

### `researchmanager.py`

Acts as the **orchestrator** of the entire research pipeline.

It coordinates:

1. Research planning
2. Search execution
3. Parallel processing
4. Result collection
5. Report generation

The manager uses asynchronous execution:

```python
results = await asyncio.gather(*tasks)
```

This allows multiple web searches to run concurrently instead of waiting for each search to finish sequentially.

---

## 🤖 AI Agents

The project separates responsibilities between different agents.

| Agent                | Responsibility                                   |
| -------------------- | ------------------------------------------------ |
| **Planner Agent**    | Creates an optimized research plan               |
| **Search Agent**     | Performs web searches and processes results      |
| **Writer Agent**     | Synthesizes research results into a final report |
| **Research Manager** | Orchestrates the complete workflow               |

This separation of responsibilities is one of the key concepts in **Agentic AI**.

---

## 🧠 Structured Output

The Planner Agent needs to produce structured research plans.

The expected structure is:

```json
{
  "searches": [
    {
      "reason": "Find the most widely used AI agent frameworks.",
      "query": "most popular AI agent frameworks 2026"
    },
    {
      "reason": "Compare the major frameworks.",
      "query": "AI agent framework comparison 2026"
    }
  ]
}
```

The data is validated using **Pydantic**:

```python
plan = WebSearchPlan.model_validate_json(content)
```

This makes the output more reliable than simply relying on free-form text.

---

## ⚡ Parallel Web Searching

One of the important parts of the project is parallel execution.

Instead of doing:

```python
result1 = await search(item1)
result2 = await search(item2)
result3 = await search(item3)
```

the project uses:

```python
tasks = [
    search(item)
    for item in plan.searches
]

results = await asyncio.gather(*tasks)
```

Conceptually:

```text
Sequential:

Search 1 ───────►
                  Search 2 ───────►
                                   Search 3 ───────►


Parallel:

Search 1 ─────────────►
Search 2 ───────────►
Search 3 ───────────────►
```

This can significantly reduce the total research time.

---

## 🛠️ Technologies

The project is built with:

* **Python**
* **OpenAI Agents SDK**
* **OpenRouter**
* **MiniMax M2.7**
* **Pydantic**
* **DuckDuckGo Search**
* **asyncio**
* **Gradio**
* **python-dotenv**

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

```bash
cd YOUR_REPOSITORY
```

---

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt` yet, you can install the main dependencies with:

```bash
pip install openai-agents openai python-dotenv gradio ddgs pydantic
```

---

## 🔑 API Configuration

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
```

The application loads the API key using:

```python
from dotenv import load_dotenv

load_dotenv()
```

and:

```python
import os

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
```

### ⚠️ Important

Never commit your `.env` file to GitHub.

Add the following to `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

---

## ▶️ Running the Application

Start the Gradio application:

```bash
python app.py
```

Gradio will provide a local URL similar to:

```text
http://127.0.0.1:7860
```

Open the URL in your browser and enter a research question.

For example:

```text
What are the most popular AI Agent frameworks in 2026?
```

---

## 🔄 Example Workflow

Suppose the user asks:

```text
What are the most popular AI Agent frameworks in 2026?
```

The system performs the following steps:

### Step 1 — Planning

The Planner Agent generates several search queries.

```text
Planning the research...
```

### Step 2 — Web Search

The Search Agent performs the generated searches.

```text
Searching the web...
```

Multiple searches can run concurrently.

### Step 3 — Collecting Results

The system gathers the results from all searches.

```text
All web searches completed.
```

### Step 4 — Writing

The Writer Agent analyzes the collected information.

```text
Writing the final report...
```

### Step 5 — Final Report

The system produces the final research report.

```text
Research complete.
```

---

## 🎯 Learning Objectives

This project was created as a practical implementation of several **Agentic AI** concepts:

* AI Agents
* Agent orchestration
* Multi-agent systems
* Function tools
* Structured outputs
* Pydantic models
* Async programming
* Parallel execution
* Web search
* LLM-based research
* Agent specialization
* Gradio interfaces

It is particularly useful for understanding how individual AI agents can be combined into a larger autonomous workflow.

---

## 🔮 Future Improvements

Possible future improvements include:

* [ ] Streaming search results to the UI
* [ ] Better source citation and reference management
* [ ] Search result deduplication
* [ ] More advanced research planning
* [ ] Research quality evaluation
* [ ] Fact-checking agent
* [ ] Source credibility scoring
* [ ] RAG integration
* [ ] Vector database integration
* [ ] Persistent research history
* [ ] Support for multiple LLM providers
* [ ] Improved error handling and retry mechanisms
* [ ] Export reports to PDF/Markdown
* [ ] Multi-language research support

---

## 📚 Inspiration

This project is inspired by concepts from the **Agentic AI** ecosystem and was developed as a learning project to understand practical multi-agent orchestration with Python.

---

## 👩‍💻 Author

**Fateme**

Master's Student in Software Engineering
Interested in:

* Artificial Intelligence
* Large Language Models
* Agentic AI
* Natural Language Processing
* Retrieval-Augmented Generation (RAG)
* Python

---

## ⭐ Contributing

Contributions, ideas, and suggestions are welcome.

If you find this project useful, consider giving it a ⭐ on GitHub.

---

## 📄 License

This project is intended primarily for educational and research purposes.

You can add a specific open-source license such as **MIT License** if you want to make the project's reuse terms explicit.
