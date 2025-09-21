from typing import Any, Callable, Dict, List, Optional
import os
import atexit
from contextlib import suppress

from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from .custom_agents import google_search_agent

# ──────────────────────────────────────────────────────────────────────────────
# MCP (Toolbox) client — used ONLY for hotel search
# ──────────────────────────────────────────────────────────────────────────────
from toolbox_core import ToolboxSyncClient

TOOLBOX_URL = os.getenv("TOOLBOX_URL", "http://127.0.0.1:5000")
toolbox = ToolboxSyncClient(TOOLBOX_URL)

def _close_toolbox() -> None:
    with suppress(Exception):
        close = getattr(toolbox, "close", None)
        if callable(close):
            close()
        else:
            client = getattr(toolbox, "_client", None)
            if client and hasattr(client, "close"):
                client.close()

atexit.register(_close_toolbox)

# ──────────────────────────────────────────────────────────────────────────────
# Tiny ADK tool wrapper (version-tolerant) + schema for hotel search
# ──────────────────────────────────────────────────────────────────────────────
def _mk_schema(props: Dict[str, Dict[str, Any]], req: List[str]) -> Dict[str, Any]:
    return {"type": "object", "properties": props, "required": req, "additionalProperties": False}

SCHEMA_hotels = _mk_schema(
    {
        "city_name": {"type": "string"},
        "location_type": {"type": "string"},
        "max_price": {"type": "number"},
    },
    ["city_name"],
)

def _make_json_tool(name: str, description: str, parameters: Dict[str, Any], executor: Callable[..., Any]):
    try:
        import google.adk.tools as tools
    except Exception as e:
        print(f"[ADK] google.adk.tools not importable; cannot register '{name}': {e}")
        return None

    candidates = [getattr(tools, n, None) for n in ("JsonSchemaFunctionTool","JsonFunctionTool","FunctionTool","ToolFn")]
    candidates = [c for c in candidates if c]

    def _try(Cls, *args, **kwargs):
        try: return Cls(*args, **kwargs)
        except Exception: return None

    trials = [
        lambda Cls: _try(Cls, fn=executor, parameters=parameters, description=description, name=name),
        lambda Cls: _try(Cls, function=executor, parameters=parameters, description=description, name=name),
        lambda Cls: _try(Cls, executor, parameters, description, name),
        lambda Cls: _try(Cls, name, description, executor, parameters),
        lambda Cls: _try(Cls, func=executor, parameters=parameters, description=description, name=name),
        lambda Cls: _try(Cls, name=name, description=description, parameters=parameters, fn=executor),
    ]
    for Cls in candidates:
        for build in trials:
            t = build(Cls)
            if t is not None:
                print(f"[ADK] Tool registered: {name} via {Cls.__name__}")
                return t
    print(f"[ADK] FAILED to register tool: {name}")
    return None

# Executor: call your Toolbox tool exactly as in tools.yaml ("search-hotels")
def exec_search_hotels(city_name: str, location_type: Optional[str] = None, max_price: Optional[float] = None) -> Any:
    # Always hit the hyphenated tool name; that’s what your YAML defines.
    return toolbox.run_tool(
        "search-hotels",
        {"city_name": city_name, "location_type": location_type, "max_price": max_price},
    )

# Register both underscore and hyphen names on the ADK side, so the LLM can call either.
mcp_hotel_tools: List[Any] = [
    _make_json_tool("search_hotels", "Search hotels in a city (MCP).", SCHEMA_hotels, exec_search_hotels),
    _make_json_tool("search-hotels", "(alias) Search hotels in a city (MCP).", SCHEMA_hotels, exec_search_hotels),
]
mcp_hotel_tools = [t for t in mcp_hotel_tools if t]  # drop Nones if any


# ──────────────────────────────────────────────────────────────────────────────
# Your original agents (unchanged logic)
# ──────────────────────────────────────────────────────────────────────────────

# Step 1: Trip Basics Collection Agent
trip_basics_agent = LlmAgent(
    name="trip_basics_collection_agent",
    model="gemini-2.5-pro",
    instruction="""You are the first agent in a sequence to plan a trip.
Your goal is to collect the basic information for the trip.
You need to collect the following information:
- Origin city/airport
- Destination country/city
- Travel dates and total number of days
- Traveler details (number of adults, children and their ages)
- Budget mindset (Frugal, Moderate, or Premium)
- Travel pace (Relaxed, Sightseeing-heavy, or Hybrid)
- For toddlers: nap windows and accessibility needs (stroller)
- Dietary preferences.

Start by greeting the user warmly and introducing your role before asking the first question.

Ask questions one by one to get this information from the user.
Once you have all the information, confirm it with the user and pass it to the next agent.
""",
    description="Collects basic trip information from the user.",
)

# Step 2: Destination Education Agent
destination_education_agent = LlmAgent(
    name="destination_education_agent",
    model="gemini-2.5-pro",
    instruction="""You are the second agent in a sequence to plan a trip.
Your goal is to educate the user about the destination they chose and help them discover popular cities.
You will receive the trip basics, including the destination country/city.

Your responsibilities are:
- Present popular cities within the selected destination.
- For each city, provide a concise "vibe" and pros/cons, especially for a family with a toddler (if applicable based on traveler details).
- Use the available tools to find this information.
- Ask the user which cities resonate with them.
- You can also handle requests for alternative cities.
""",
    description="Educates the user about the destination and helps select cities.",
    tools=[agent_tool.AgentTool(agent=google_search_agent)]
)

# Step 3: City Selection Agent
city_selection_agent = LlmAgent(
    name="city_selection_agent",
    model="gemini-2.5-pro",
    instruction="""You are the third agent in a sequence to plan a trip.
Your goal is to finalize city selection and propose an itinerary split.

Your responsibilities are:
- Propose 1-2 city splits for the given duration
- Provide rationale for city combinations
- Validate transit times and practicality for toddlers (if applicable)
- Get user confirmation on city selection
- Adjust based on user feedback
- Use Google Search to find transit information between cities

You will receive:
- Trip basics (dates, duration, traveler details)
- City preferences from the previous agent

Output a structured city selection with duration split and rationale.
""",
    description="Finalizes city selection and proposes itinerary split.",
    tools=[agent_tool.AgentTool(agent=google_search_agent)]
)

# Step 4: Activity Discovery Agent
activity_discovery_agent = LlmAgent(
    name="activity_discovery_agent",
    model="gemini-2.5-pro",
    instruction="""You are the fourth agent in a sequence to plan a trip.
Your goal is to discover and select kid-friendly activities per chosen city.

Your responsibilities are:
- Suggest kid-friendly activities for each chosen city
- Tag activities with: indoor/outdoor, shaded, short-walk, stroller-friendly, toddler-friendly
- Provide "why" notes for each suggestion
- Offer backups for weather or nap conflicts
- Allow user to accept/decline and refine selection
- Use Google Search to find current activity information, reviews, and details

You will receive:
- Confirmed cities and trip preferences
- Traveler details including ages

Output selected activities with tags and rationales for each city.
""",
    description="Discovers and selects kid-friendly activities per city.",
    tools=[agent_tool.AgentTool(agent=google_search_agent)]
)

# Step 5: Hotel Shortlisting Agent (ONLY place we add MCP tools)
# Keep Google Search tool, and ADD the MCP tools so the model can call:
#   - search_hotels  (ADK tool name)
#   - search-hotels  (ADK alias)
# The executor behind both hits your Toolbox tool "search-hotels" from tools.yaml.
hotel_shortlisting_agent = LlmAgent(
    name="hotel_shortlisting_agent",
    model="gemini-2.5-pro",
    instruction="""You are the fifth agent in a sequence to plan a trip.
Your goal is to search and shortlist hotels for the chosen cities.

Your responsibilities are:
- Ask for location preferences (central/airport/beach)
- Get room type requirements
- Identify must-haves (crib, kitchenette, pool, family-friendly amenities)
- Use BOTH the attached MCP tools (search_hotels / search-hotels) and Google Search to find hotels
- Present 3-5 hotels with rationale for each city
- Provide booking links and detailed information
- Consider family needs and toddler requirements

You will receive:
- Selected cities, dates, and hotel preferences
- Traveler details and requirements

Output hotel shortlist with prices, amenities, and booking information.
""",
    description="Searches and shortlists hotels using MCP + web.",
    tools=[agent_tool.AgentTool(agent=google_search_agent)] + mcp_hotel_tools,
)

# Step 6: Flight Shortlisting Agent
flight_shortlisting_agent = LlmAgent(
    name="flight_shortlisting_agent",
    model="gemini-2.5-pro",
    instruction="""You are the sixth agent in a sequence to plan a trip.
Your goal is to search and shortlist flights for the trip.

Your responsibilities are:
- Ask for departure time preferences
- Get stop preferences (non-stop vs connecting)
- Identify baggage needs and special requirements
- Use Google Search to find current flight options and prices
- Present options with duration/price trade-offs
- Check cost sensitivity and provide guidance
- Consider toddler travel needs (timing, stops, comfort)
- Allow sorting by price or duration

You will receive:
- Origin, destination, dates, and flight preferences
- Traveler details and requirements

Output flight shortlist with cost/duration analysis and recommendations.
""",
    description="Searches and shortlists flights using real-time data.",
    tools=[agent_tool.AgentTool(agent=google_search_agent)]
)

# Step 7: Itinerary Generation Agent
itinerary_generation_agent = LlmAgent(
    name="itinerary_generation_agent",
    model="gemini-2.5-pro",
    instruction="""You are the seventh and final agent in a sequence to plan a trip.
Your goal is to compose a complete day-by-day itinerary.

Your responsibilities are:
- Create detailed daily schedules for each city
- Respect nap windows and walking limits for toddlers
- Include travel times between activities
- Add weather considerations and backups
- Provide rain-safe alternatives
- Allow scoped edits (swap activity, adjust time)
- Generate cost overview
- Use Google Search for weather forecasts and local information
- Consider opening hours, best times to visit, and local tips

You will receive:
- All previous step outputs (cities, activities, hotels, flights)
- Complete trip context

Output a complete itinerary with:
- Day-by-day detailed schedule
- Cost breakdown
- Weather considerations
- Backup plans
- Practical tips and recommendations
""",
    description="Composes final day-by-day itinerary with all details.",
    tools=[agent_tool.AgentTool(agent=google_search_agent)]
)

# Coordinator
trip_planner_agent = LlmAgent(
    name="trip_planner_coordinator",
    model="gemini-2.5-pro",
    instruction="""You are a coordinator agent for a comprehensive trip planning service.
Your job is to manage a sequence of 7 sub-agents to help a user plan a complete trip.
You must execute the agents in the following strict order:

1. trip_basics_collection_agent: Collect basic trip information (origin, destination, dates, travelers, budget, etc.)
2. destination_education_agent: Educate user about destination and discover popular cities
3. city_selection_agent: Finalize city selection and propose itinerary split
4. activity_discovery_agent: Discover and select kid-friendly activities per city
5. hotel_shortlisting_agent: Search and shortlist hotels for chosen cities
6. flight_shortlisting_agent: Search and shortlist flights for the trip
7. itinerary_generation_agent: Compose final day-by-day itinerary with all details

Each agent will build upon the previous agent's output to create a complete trip plan.
You should not interact with the user directly. You should delegate the tasks to the sub-agents in sequence.
Start by calling the trip_basics_collection_agent.

The workflow is designed to be family-friendly, especially considering toddlers and their specific needs.
""",
    description="A comprehensive coordinator agent for complete trip planning with 7 sequential steps.",
    sub_agents=[
        trip_basics_agent,
        destination_education_agent,
        city_selection_agent,
        activity_discovery_agent,
        hotel_shortlisting_agent,
        flight_shortlisting_agent,
        itinerary_generation_agent,
    ]
)

root_agent = trip_planner_agent
