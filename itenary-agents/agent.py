from google.adk.agents import LlmAgent
 

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
)


# This is the main coordinator agent that will manage the sequential workflow.
trip_planner_agent = LlmAgent(
    name="trip_planner_coordinator",
    model="gemini-2.5-pro",
    instruction="""You are a coordinator agent for a trip planning service.
Your job is to manage a sequence of sub-agents to help a user plan a trip.
You must execute the agents in the following order:
1. trip_basics_collection_agent: to collect basic trip information.
2. destination_education_agent: to help the user choose cities.

You should not interact with the user directly. You should delegate the tasks to the sub-agents.
Start by calling the trip_basics_collection_agent.
""",
    description="A coordinator agent for the trip planner.",
    sub_agents=[
        trip_basics_agent,
        destination_education_agent,
    ]
)

root_agent = trip_planner_agent
