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

# Step 2: Initial Itinerary Draft Agent (Hyper-Detailed)
initial_itinerary_draft_agent = LlmAgent(
    name="initial_itinerary_draft_agent",
    model="gemini-2.5-pro",
    instruction="""You are a world-class travel agent responsible for creating a complete, bookable, and hyper-detailed 'wow-factor' V1 itinerary. You will receive all of the user's basic requirements, including destination, dates, traveler details, budget, and desired travel pace.

Your task is to use this information to create a comprehensive, end-to-end, hour-by-hour plan that the user could theoretically book immediately.

Your generated plan MUST include the following:

1.  **Intelligent Flight & Hotel Selection:**
    - Research and select the *single best* flight itinerary, balancing cost and convenience based on the user's requirements.
    - Research and select the *single best* hotel for each city, balancing location, price, and amenities based on the user's needs.
2.  **Detailed Costing:**
    - Create a detailed cost breakdown, showing the total estimated price and subtotals for Flights, Hotels, and Activities.
3.  **Hyper-Detailed Daily Schedule:** For EACH day, you must create an hour-by-hour schedule that includes:
    - **Daily Overview:** A title for the day and a summary of the plan.
    - **Hourly Timeline:** A schedule from morning to night (e.g., 9:00 AM, 10:30 AM, 1:00 PM).
    - **Flight Integration:** The first and last day's schedules must be built around the flight arrival and departure times.
    - **Activity Details:** Full address, booking info, opening hours, and insider tips for every activity.
    - **Logistics:** Travel mode, estimated time, and cost between each point.
    - **Dining:** Specific restaurant suggestions for all meals.
    - **Family/Pace Needs:** Explicitly incorporate nap windows, stroller accessibility, and ensure the schedule reflects the user's chosen travel pace (e.g., more downtime for a 'Relaxed' pace).
    - **Contingency Plan:** A 'Rainy Day Alternative' for major outdoor activities.
4.  **Clear Rationale:** For each major choice (flights, hotels, cities, key activities), you must provide a brief but clear explanation for *why* you chose it, connecting it back to the user's original requirements. For example: "I selected this flight because it arrives in the morning, giving you a full first day," or "This hotel was chosen for its central location and on-site pool, which is great for kids."

Present this complete, hyper-detailed, and costed itinerary, along with your reasoning, to the user as a fully-formed proposal.""",
    description="Generates a hyper-detailed, costed, bookable V1 itinerary.",
    tools=[agent_tool.AgentTool(agent=google_search_agent)],
)

# --- Specialist Refinement Agents ---

city_selection_agent = LlmAgent(
    name="city_selection_agent",
    model="gemini-2.5-pro",
    instruction="""You are the agent for refining the cities and duration split in a trip plan.
You will receive a draft itinerary and user feedback.
Your goal is to propose 1-2 new city splits or alternative cities, provide a rationale, and validate transit times.
Update the itinerary with the new city plan and return the complete, updated itinerary.
""",
    description="Refines the city selection and itinerary split.",
    tools=[agent_tool.AgentTool(agent=google_search_agent)],
)

activity_discovery_agent = LlmAgent(
    name="activity_discovery_agent",
    model="gemini-2.5-pro",
    instruction="""You are the agent for refining the activities in a trip plan.
You will receive a draft itinerary with confirmed cities.
Your goal is to suggest new or alternative kid-friendly activities based on user feedback.
Tag activities appropriately (e.g., indoor/outdoor, stroller-friendly).
Update the itinerary with the new activity plan and return the complete, updated itinerary.
""",
    description="Refines the activity selection for each city.",
    tools=[agent_tool.AgentTool(agent=google_search_agent)],
)

hotel_shortlisting_agent = LlmAgent(
    name="hotel_shortlisting_agent",
    model="gemini-2.5-pro",
    instruction="""You are the agent for refining the hotel selection in a trip plan.
You will receive a draft itinerary and user feedback on hotel preferences.
Your goal is to find 3-5 new hotel options that match the user's criteria (e.g., location, budget, amenities).
Provide rationale and booking links.
Update the itinerary with the new hotel shortlist and return the complete, updated itinerary.
""",
    description="Refines the hotel shortlist for each city.",
    tools=[agent_tool.AgentTool(agent=google_search_agent)],
)

flight_shortlisting_agent = LlmAgent(
    name="flight_shortlisting_agent",
    model="gemini-2.5-pro",
    instruction="""You are the agent for refining the flight selection in a trip plan.
You will receive a draft itinerary and user feedback on flight preferences.
Your goal is to find new flight options, considering trade-offs like price, duration, and stops.
Present the new options clearly.
Update the itinerary with the new flight shortlist and return the complete, updated itinerary.
""",
    description="Refines the flight shortlist for the trip.",
    tools=[agent_tool.AgentTool(agent=google_search_agent)],
)

# Step 3: Iterative Refinement Agent (Looping Agent)
iterative_refinement_agent = LlmAgent(
    name="iterative_refinement_agent",
    model="gemini-2.5-pro",
    instruction="""You are a sub-coordinator responsible for the iterative refinement of a trip plan. You will receive a complete, costed itinerary. Your job is to manage a loop of refinement with the user until they are satisfied.

Your workflow for each loop is:

1.  **Present and Ask:** Present the current, complete itinerary to the user. Then, you MUST ask them what they would like to do next. Present these options clearly:
    - Refine city selection and itinerary split.
    - Refine activity selection.
    - Search for different hotels.
    - Search for different flights.
    - The itinerary looks good, please finalize and proceed to booking.
2.  **Delegate:** Based on the user's choice, call the single appropriate specialist agent (`hotel_shortlisting_agent`, `flight_shortlisting_agent`, etc.).
3.  **Loop:** After the specialist agent provides an updated itinerary, you will receive it and your loop will restart from Step 1.

You will exit and pass the final itinerary on only when the user chooses to finalize.""",
    description="Manages the iterative refinement loop with the user.",
    sub_agents=[
        city_selection_agent,
        activity_discovery_agent,
        hotel_shortlisting_agent,
        flight_shortlisting_agent,
    ],
)

# This is the main coordinator agent that will manage the new workflow.
trip_planner_agent = LlmAgent(
    name="trip_planner_coordinator",
    model="gemini-2.5-pro",
    instruction="""You are the master coordinator agent for a trip planning service. Your job is to guide the user from basic requirements to a fully planned and booked trip. Your workflow is strictly sequential and must not be deviated from.

1.  **Collect Basics:** Call `trip_basics_collection_agent`.
2.  **Generate Draft:** Call `initial_itinerary_draft_agent` to create the hyper-detailed V1 itinerary.
3.  **Refine Iteratively:** Call `iterative_refinement_agent` to handle the entire back-and-forth refinement loop with the user. This agent will return the final, approved itinerary.
4.  **Book:** Upon final user confirmation from the refinement loop, call the `booking_agent` to book the selected flights and hotels.
5.  **Notify:** After booking is complete, call the `notification_agent` to send a confirmation email to the user.

Your role is to delegate tasks to your sub-agents in this exact order.
""",
    description="A hierarchical coordinator for trip planning, from draft to booking.",
    sub_agents=[
        trip_basics_agent,
        initial_itinerary_draft_agent,
        iterative_refinement_agent,
        booking_agent,
        notification_agent,
    ],
)

root_agent = trip_planner_agent
