from typing import Any

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import ChatOpenAI
from tavily import TavilyClient

load_dotenv()

SYSTEM_PROMPT = """You are a personal chef. The user will tell you what ingredients
they have at home. Use the web search tool to find recipes that fit those
ingredients. Suggest recipes clearly, and provide instructions when requested.
"""


@tool("tavily_web_search", description="Use Tavily to search the web for information")
def web_search(query: str) -> dict[str, Any]:
    """Search the web for recipe information."""
    return TavilyClient().search(query)


def build_agent():
    """Create the chef agent with an in-memory conversation checkpointer."""
    model = ChatOpenAI(
        model="gpt-5.6-luna",
        use_responses_api=True,
        temperature=0.2,
    )

    return create_agent(
        model=model,
        tools=[web_search],
        system_prompt=SYSTEM_PROMPT,
        checkpointer=InMemorySaver(),
    )
