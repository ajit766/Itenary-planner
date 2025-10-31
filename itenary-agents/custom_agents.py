from google.adk.agents import Agent
from google.adk.tools import google_search, FunctionTool


def tool(func):
    """Decorator to wrap a function as a FunctionTool."""
    return FunctionTool(func=func)


# Create an agent with google search tool as a search specialist
google_search_agent = Agent(
    model='gemini-2.5-flash',
    name='google_search_agent',
    description='A search agent that uses google search to get any information user asks',
    instruction='Use google search to find information related to anything',
    tools=[google_search],
)


@tool
def book_flights(itinerary: dict) -> str:
    """Books flights for the given itinerary."""
    print(f"Booking flights for: {itinerary}")
    return "Flights booked successfully!"


@tool
def book_hotels(itinerary: dict) -> str:
    """Books hotels for the given itinerary."""
    print(f"Booking hotels for: {itinerary}")
    return "Hotels booked successfully!"


@tool
def send_email(recipient: str, subject: str, body: str) -> str:
    """Sends an email to the user with the booking confirmation."""
    print(f"Sending email to: {recipient}")
    return "Email sent successfully!"


booking_agent = Agent(
    model='gemini-2.5-flash',
    name='booking_agent',
    description='An agent that books flights and hotels for the user.',
    instruction='Use the available tools to book flights and hotels for the user.',
    tools=[book_flights, book_hotels],
)

notification_agent = Agent(
    model='gemini-2.5-flash',
    name='notification_agent',
    description='An agent that sends a confirmation email to the user.',
    instruction='Use the available tools to send a confirmation email to the user.',
    tools=[send_email],
)
