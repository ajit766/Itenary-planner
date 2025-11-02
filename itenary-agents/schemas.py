from pydantic import BaseModel, Field
from typing import List, Optional

class Flight(BaseModel):
    airline: str
    flight_number: str
    departure_time: str
    arrival_time: str
    price: float

class Hotel(BaseModel):
    name: str
    address: str
    price_per_night: float

class Activity(BaseModel):
    name: str
    start_time: str
    end_time: str
    description: str
    cost: float

class DailyPlan(BaseModel):
    day: int
    theme: str
    activities: List[Activity]

class Itinerary(BaseModel):
    origin: str
    destination: str
    total_cost: float
    flights: Flight
    hotel: Hotel
    daily_plans: List[DailyPlan]
    rationale: str = Field(description="The reasoning behind the choices made in this itinerary.")
