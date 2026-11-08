# Personal Chef

A personal-chef AI agent built with LangChain. It accepts a text request, uses a Tavily web-search tool to find recipe ideas, and keeps conversation context in memory for the lifetime of the running process.

## What this example demonstrates

- Creating an agent with LangChain's `create_agent`
- Defining a custom Tavily search tool
- Connecting to an OpenAI model through `ChatOpenAI`
- Using a system prompt to guide the agent
- Keeping conversation history with LangGraph's `InMemorySaver` and a thread ID

## Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)
- An OpenAI API key
- A Tavily API key

## Setup

uv sync creates the project’s .venv and installs dependencies from `pyproject.toml`.

```bash
uv sync
```

Create your local environment file from the example:

```bash
cp .env.example .env
```

Edit `.env` and replace the placeholders with your API keys:

```dotenv
OPENAI_API_KEY=your-openai-api-key
TAVILY_API_KEY=your-tavily-api-key
```

## Run

uv run runs the command in the virtual environment automatically

```bash
uv run python chef.py
```

The script asks for recipe ideas using leftover chicken and rice, then asks a follow-up question. Both requests use the same thread ID, so the agent can refer to the ingredients from the first request in its second response.

## Configuration

The example configures the model in `chef.py`:

```python
ChatOpenAI(
    model="gpt-5.6-luna",
    use_responses_api=True,
    temperature=0.2,
)
```

Change the model name there if you want to try another model available to your OpenAI account.

The agent uses Tavily for web search, so both API keys must be set even though only the OpenAI key is used to generate responses.

## Memory behavior

`InMemorySaver` stores conversation state only in memory. The same `thread_id` lets the two calls in this script share conversation history. The memory is lost when the process exits; it is not persistent storage across runs.

## Project layout

```text
personal-chef/
├── chef.py            # LangChain agent example
├── pyproject.toml     # Project metadata and dependencies
├── uv.lock            # Locked dependency versions
├── .env.example       # Environment variable template
└── README.md
```

## Troubleshooting

- **Missing API key:** Check that `.env` exists in the project root and contains valid `OPENAI_API_KEY` and `TAVILY_API_KEY` values.

- **Dependency changes:** After changing dependencies in `pyproject.toml`, run `uv sync` to update the environment and lock file.

- **Build error about package discovery:** This project currently runs a standalone script rather than installing a Python package. The `[tool.setuptools] py-modules = []` setting in `pyproject.toml` tells setuptools not to guess which top-level scripts should be packaged. Keep it while the project has no importable package under `src/`.
