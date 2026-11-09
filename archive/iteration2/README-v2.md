# Personal Chef

A personal-chef AI agent built with LangChain and Streamlit. It accepts text requests, uses a Tavily web-search tool to find recipe ideas, and keeps conversation context in memory while the app is running.

## What this project demonstrates

- Creating an agent with LangChain's `create_agent`
- Defining a custom Tavily search tool
- Connecting to an OpenAI model through `ChatOpenAI`
- Guiding the agent with a system prompt
- Keeping conversation history with LangGraph's `InMemorySaver` and a thread ID
- Building a chat interface with Streamlit

## Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)
- An OpenAI API key
- A Tavily API key

## Setup

Install the project and its dependencies. `uv sync` creates the project's `.venv` automatically:

```bash
uv sync
```

Create a local environment file and add your API keys:

```bash
cp .env.example .env
```

```dotenv
OPENAI_API_KEY=your-openai-api-key
TAVILY_API_KEY=your-tavily-api-key
```

Keep `.env` private; it is excluded from Git.

## Run

Launch the Streamlit app from the project root:

```bash
uv run streamlit run streamlit_app.py
```

The app opens in your browser. Enter your ingredients, then ask follow-up questions in the same conversation. Choose **New conversation** to start a fresh thread.

## Configuration

The model is configured in `src/chef_agent/chef.py`:

```python
ChatOpenAI(
    model="gpt-5.6-luna",
    use_responses_api=True,
    temperature=0.2,
)
```

Change the model name there to try another model available to your OpenAI account. Tavily powers web search, so both API keys must be set.

## Memory behavior

`InMemorySaver` stores conversation state only in memory. Streamlit assigns a thread ID to each browser session, so follow-up messages in that session share context. The memory is lost when the app process exits; it is not persistent storage across runs.

## Project layout

```text
personal-chef/
├── src/
│   └── chef_agent/
│       ├── __init__.py
│       └── chef.py
├── streamlit_app.py
├── pyproject.toml
├── uv.lock
├── .env.example
├── .gitignore
└── README.md
```

`chef_agent` contains the reusable agent code. `streamlit_app.py` is the UI entry point.

## Troubleshooting

- **Missing API key:** Check that `.env` exists in the project root and contains valid `OPENAI_API_KEY` and `TAVILY_API_KEY` values.
- **Dependency changes:** After changing dependencies in `pyproject.toml`, run `uv lock` to update `uv.lock`, then `uv sync` to update the environment.
