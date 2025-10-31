from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from .custom_agents import google_search_agent, booking_agent, notification_agent


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

# Step 2: Itinerary Proposer Agent
itinerary_proposer_agent = LlmAgent(
    name="itinerary_proposer_agent",
    model="gemini-2.5-pro",
    instruction="""You are the second agent in a sequence to plan a trip.
Your goal is to generate a complete, initial itinerary based on the user's preferences.
You will receive the trip basics from the previous agent.

Your responsibilities are:
- Propose a complete itinerary including cities, activities, hotels, and flights.
- Explain your choices to the user, highlighting why they are a good fit for their needs (especially for families with toddlers).
- Present the itinerary in a clear, day-by-day format.
- Use the available tools to find the best options for flights, hotels, and activities.
- After presenting the itinerary, ask the user for their feedback.
""",
    description="Generates an initial itinerary and explains the choices to the user.",
    tools=[agent_tool.AgentTool(agent=google_search_agent)]
)

# Step 3: Itinerary Refinement Agent
itinerary_refinement_agent = LlmAgent(
    name="itinerary_refinement_agent",
    model="gemini-2.5-pro",
    instruction="""You are the third agent in a sequence to plan a trip.
Your goal is to refine the itinerary based on user feedback.
You will receive the initial itinerary and the user's feedback.

Your responsibilities are:
- Modify the itinerary based on the user's requests (e.g., change cities, activities, hotels, or flights).
- Use the available tools to find new options that match the user's feedback.
- Present the updated itinerary to the user.
- Continue this process until the user is satisfied with the plan.
- Once the user is happy, ask for confirmation to proceed with booking.
""",
    description="Refines the itinerary based on user feedback.",
    tools=[agent_tool.AgentTool(agent=google_search_agent)]
)

# This is the main coordinator agent that will manage the new workflow.
trip_planner_agent = LlmAgent(
    name="trip_planner_coordinator",
    model="gemini-2.5-pro",
    instruction="""You are a coordinator agent for a comprehensive trip planning service.
Your job is to manage a sequence of agents to help a user plan and book a complete trip.
You must execute the agents in the following order:

1. trip_basics_collection_agent: Collect basic trip information.
2. itinerary_proposer_agent: Generate a complete initial itinerary and present it to the user.
3. itinerary_refinement_agent: Handle user feedback and refine the itinerary until the user is satisfied.
4. booking_agent: Once the user confirms, book the flights and hotels.
5. notification_agent: Send a confirmation email to the user with all the details.

You should not interact with the user directly. You should delegate the tasks to the sub-agents in sequence.
Start by calling the trip_basics_collection_agent.
""",
    description="A comprehensive coordinator agent for complete trip planning and booking.",
    sub_agents=[
        trip_basics_agent,
        itinerary_proposer_agent,
        itinerary_refinement_agent,
        booking_agent,
        notification_agent,
    ]
)

root_agent = trip_planner_agent