from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from langchain_openai import ChatOpenAI

from typing import Dict, Any
from tavily import TavilyClient


##################################################################################################

@tool("tavily_web_search", description="Use Tavily to search the web for information")
def web_search(query: str) -> Dict[str, Any]:

    """Search the web for information"""

    return TavilyClient().search(query)


##################################################################################################


system_prompt = """

You are a personal chef. The user will give you a list of ingredients they have left over in their house.

Using the web search tool, search the web for recipes that can be made with the ingredients they have.

Return recipe suggestions and eventually the recipe instructions to the user, if requested.

"""

checkpointer = InMemorySaver()

##################################################################################################


model = ChatOpenAI(
    model="gpt-5.6-luna",
    use_responses_api=True,
    temperature=0.2
)

##################################################################################################

agent = create_agent(
    model=model,
    tools=[web_search],
    system_prompt=system_prompt,
    checkpointer=checkpointer
)

##################################################################################################


config = {"configurable": {"thread_id": "1"}}

first_response = agent.invoke(
    {
        "messages": [
            HumanMessage(content="I have leftover chicken and rice. What can I make?")
        ]
    },
    config=config,
)
print("First response:")
print(first_response["messages"][-1].text)

second_response = agent.invoke(
    {
        "messages": [
            HumanMessage(content="What ingredients did I say I had?")
        ]
    },
    config=config,
)
print("Second response:")
print(second_response["messages"][-1].text)