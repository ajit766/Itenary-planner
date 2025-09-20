from google.adk.agents import Agent
from google.adk.tools import google_search


# Create an agent with google search tool as a search specialist
google_search_agent = Agent(
    model='gemini-2.5-flash',
    name='google_search_agent',
    description='A search agent that uses google search to get any information user asks',
    instruction='Use google search to find information related to anything',
    tools=[google_search],
)