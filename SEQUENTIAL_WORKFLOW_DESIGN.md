# Trip Planner MVP - Sequential Workflow Agent Design

## 🎯 **Selected Architecture: Sequential Workflow Agent**

```
Sequential Workflow Agent
├── Step 1: Trip Basics Collection
├── Step 2: Destination Education
├── Step 3: City Selection
├── Step 4: Activity Discovery
├── Step 5: Hotel Shortlisting
├── Step 6: Flight Shortlisting
└── Step 7: Itinerary Generation
```

## 🔄 **Sequential Workflow Steps**

### **Step 1: Trip Basics Collection Agent**
**Purpose:** Collect fundamental trip information from user

**Responsibilities:**
- Ask for origin city/airport
- Collect destination country/city (user input)
- Gather travel dates and total days
- Get traveler details (count, ages, including toddler info)
- Determine budget mindset (Frugal/Moderate/Premium)
- Identify travel pace (Relaxed/Sightseeing-heavy/Hybrid)
- Collect nap windows and accessibility needs
- Get dietary preferences

**Input:** User conversation
**Output:** Structured trip basics data
**MCP Tools Used:** None (pure conversation)

**Sample Flow:**
```
Agent: "Hi! I'm your trip planning assistant. Let's start with the basics. 
Where are you traveling from?"
User: "Mumbai"
Agent: "Great! And where would you like to go for your vacation?"
User: "Thailand"
Agent: "Perfect! When are you planning to travel and for how many days?"
...
```

### **Step 2: Destination Education Agent**
**Purpose:** Educate user about destination and discover popular cities

**Responsibilities:**
- Present popular cities within selected destination
- Provide concise "vibes" and pros/cons tailored for toddler
- Offer links and 1-2 short videos per city
- Ask which cities resonate with user
- Handle user requests for alternatives

**Input:** Trip basics data
**Output:** Educated user with city preferences
**MCP Tools Used:** Google Maps MCP (for city information)

**Sample Flow:**
```
Agent: "Thailand offers amazing destinations! Let me show you the top cities:

🏙️ Bangkok (3-4 days ideal)
- Pros: Great food, temples, shopping, family-friendly attractions
- Cons: Busy, hot weather, lots of walking
- Best for: Culture, food, shopping

🏝️ Phuket (2-3 days ideal)  
- Pros: Beautiful beaches, water activities, resorts
- Cons: More expensive, touristy
- Best for: Relaxation, beach time

Which cities interest you most?"
```

### **Step 3: City Selection Agent**
**Purpose:** Finalize city selection and propose itinerary split

**Responsibilities:**
- Propose 1-2 city splits for given duration
- Provide rationale for city combinations
- Validate transit times and practicality for toddler
- Get user confirmation on city selection
- Adjust based on user feedback

**Input:** City preferences from Step 2
**Output:** Confirmed city selection with duration split
**MCP Tools Used:** Google Maps MCP (for transit times)

**Sample Flow:**
```
Agent: "Based on your 6-day trip, I recommend:
📅 Bangkok (3 days) + Phuket (3 days)
- Bangkok: Explore temples, markets, food
- Phuket: Beach time, water activities
- Flight between cities: 1.5 hours (perfect for toddler)

Does this split work for you, or would you prefer a different combination?"
```

### **Step 4: Activity Discovery Agent**
**Purpose:** Discover and select kid-friendly activities per city

**Responsibilities:**
- Suggest kid-friendly activities per chosen city
- Tag activities (indoor, shaded, short-walk, stroller-friendly)
- Provide "why" notes for each suggestion
- Offer backups for weather or nap conflicts
- Allow user to accept/decline and refine selection

**Input:** Confirmed cities and trip preferences
**Output:** Selected activities with tags and rationales
**MCP Tools Used:** Google Maps MCP (Places API for POI discovery)

**Sample Flow:**
```
Agent: "Let me find kid-friendly activities in Bangkok:

🎠 Chatuchak Weekend Market
- Tags: Indoor, stroller-friendly, short-walk
- Why: Great for families, food options, shopping

🐠 Siam Ocean World
- Tags: Indoor, stroller-friendly, toddler-friendly
- Why: Perfect for 2-year-old, air-conditioned, educational

Which activities interest you? I can find more options or adjust based on your preferences."
```

### **Step 5: Hotel Shortlisting Agent**
**Purpose:** Search and shortlist hotels using EaseMyTrip

**Responsibilities:**
- Ask for location preferences (central/airport/beach)
- Get room type requirements
- Identify must-haves (crib, kitchenette, pool)
- Query EaseMyTrip MCP for hotels
- Present 3-5 hotels with rationale
- Provide deep links for booking

**Input:** Selected cities, dates, and hotel preferences
**Output:** Hotel shortlist with prices and booking links
**MCP Tools Used:** EaseMyTrip MCP (Hotels)

**Sample Flow:**
```
Agent: "Now let's find perfect hotels for your family. 
What's your preference - central location or near airport?"

User: "Central location, close to activities"

Agent: "Here are my top hotel recommendations:

🏨 Hotel A - $120/night
- Location: Central Bangkok, 10min to Chatuchak
- Family features: Crib available, kids' pool
- Why: Perfect location, family-friendly, great reviews
- [Book Now] [View Details]

🏨 Hotel B - $95/night  
- Location: Near Siam Ocean World
- Family features: Kitchenette, connecting rooms
- Why: Great value, convenient for your activities
- [Book Now] [View Details]"
```

### **Step 6: Flight Shortlisting Agent**
**Purpose:** Search and shortlist flights using EaseMyTrip

**Responsibilities:**
- Ask for departure time preferences
- Get stop preferences (non-stop vs connecting)
- Identify baggage needs
- Query EaseMyTrip MCP for flights
- Present options with duration/price trade-offs
- Check cost sensitivity and provide guidance
- Allow sorting by price or duration

**Input:** Origin, destination, dates, and flight preferences
**Output:** Flight shortlist with cost/duration analysis
**MCP Tools Used:** EaseMyTrip MCP (Flights)

**Sample Flow:**
```
Agent: "Let me find the best flights for your family:

✈️ Flight Option 1 - $450/person
- Duration: 4h 30m (non-stop)
- Departure: 10:30 AM
- Why: Perfect timing, no stops, toddler-friendly

✈️ Flight Option 2 - $380/person  
- Duration: 6h 15m (1 stop)
- Departure: 8:00 AM
- Why: 15% cheaper but longer with stop

Given you're traveling with a toddler, I recommend Option 1 for comfort. 
Are you cost-sensitive, or would you prefer the shorter journey?"
```

### **Step 7: Itinerary Generation Agent**
**Purpose:** Compose final day-by-day itinerary

**Responsibilities:**
- Create detailed daily schedules
- Respect nap windows and walking limits
- Include travel times between activities
- Add weather considerations and backups
- Provide rain-safe alternatives
- Allow scoped edits (swap activity, adjust time)
- Generate cost overview
- Create shareable link and PDF

**Input:** All previous step outputs
**Output:** Complete itinerary with cost breakdown
**MCP Tools Used:** Google Maps MCP (Directions, Weather)

**Sample Flow:**
```
Agent: "Here's your complete 6-day Thailand itinerary:

📅 Day 1 - Bangkok Arrival
- 10:30 AM: Flight arrival, check-in hotel
- 2:00 PM: Nap time (toddler)
- 4:00 PM: Chatuchak Market (2 hours)
- 6:00 PM: Dinner at hotel
- 8:00 PM: Early bedtime

📅 Day 2 - Bangkok Exploration  
- 9:00 AM: Siam Ocean World (3 hours)
- 12:00 PM: Lunch nearby
- 1:00 PM: Nap time
- 4:00 PM: Temple visit (1 hour)
- 6:00 PM: Return to hotel

Total Estimated Cost: $1,200
[Share Itinerary] [Export PDF] [Edit Day]"
```

## 🔧 **MCP Server Architecture**

### **1. EaseMyTrip MCP Server (Mock Data)**
**Purpose:** Provide flight and hotel search with mock PostgreSQL data

**Tools:**
- `search_flights(params)` - Search flights with mock data
- `search_hotels(params)` - Search hotels with mock data
- `get_flight_details(flight_id)` - Get detailed flight info
- `get_hotel_details(hotel_id)` - Get detailed hotel info

**Mock Data Structure:**
```sql
-- Flights table
CREATE TABLE flights (
    id SERIAL PRIMARY KEY,
    origin VARCHAR(3),
    destination VARCHAR(3),
    departure_time TIMESTAMP,
    arrival_time TIMESTAMP,
    duration_minutes INTEGER,
    stops INTEGER,
    airline VARCHAR(50),
    price_usd DECIMAL(10,2),
    available_seats INTEGER
);

-- Hotels table  
CREATE TABLE hotels (
    id SERIAL PRIMARY KEY,
    city VARCHAR(50),
    name VARCHAR(100),
    address TEXT,
    rating DECIMAL(2,1),
    price_usd_per_night DECIMAL(10,2),
    amenities JSONB,
    location_type VARCHAR(20), -- central, airport, beach
    family_friendly BOOLEAN
);
```

### **2. Google Maps MCP Server**
**Purpose:** Discover activities and provide location data

**Tools:**
- `search_places(city, category, filters)` - Find POIs
- `get_place_details(place_id)` - Get detailed place info
- `get_directions(origin, destination)` - Calculate travel times
- `get_city_info(city_name)` - Get city overview and attractions

**Integration:**
- Google Places API for POI discovery
- Google Directions API for travel times
- Google Geocoding API for location data

### **3. Weather MCP Server**
**Purpose:** Provide weather forecasts for itinerary planning

**Tools:**
- `get_weather_forecast(city, date)` - Get weather for specific date
- `get_weather_alerts(city)` - Check for weather warnings
- `suggest_weather_alternatives(activity, weather)` - Suggest indoor alternatives

## 🏗️ **Technical Implementation Plan**

### **Phase 1: MCP Servers (Week 1)**
1. Set up PostgreSQL with mock data
2. Create EaseMyTrip MCP server
3. Create Google Maps MCP server  
4. Create Weather MCP server
5. Test MCP tools with MCPToolbox

### **Phase 2: Sequential Workflow Agent (Week 2)**
1. Create base workflow agent structure
2. Implement Step 1: Trip Basics Collection
3. Implement Step 2: Destination Education
4. Implement Step 3: City Selection
5. Test workflow progression

### **Phase 3: Activity & Booking Agents (Week 3)**
1. Implement Step 4: Activity Discovery
2. Implement Step 5: Hotel Shortlisting
3. Implement Step 6: Flight Shortlisting
4. Test MCP integrations

### **Phase 4: Itinerary Generation (Week 4)**
1. Implement Step 7: Itinerary Generation
2. Add cost calculation
3. Implement sharing features
4. End-to-end testing

## 📋 **Approval Checklist**

Before implementation, please review:

- [ ] Sequential workflow steps make sense
- [ ] Each agent's responsibilities are clear
- [ ] MCP server design is appropriate
- [ ] Mock data structure covers required scenarios
- [ ] Integration points are well-defined
- [ ] Implementation phases are realistic

**Ready for your approval to proceed with implementation! 🚀**
