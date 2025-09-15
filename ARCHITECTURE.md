# Trip Planner MVP — Technical Architecture (Conversation-First)

## 1) Overview
Conversation-first web app where the AI interviews the traveler, educates them about destination choices, shortlists hotels and flights via EaseMyTrip (EMT), and composes a kid-friendly itinerary. Places to visit are discovered collaboratively during the chat.

## 2) High-Level Components
- Frontend (Next.js + TypeScript)
  - Chat UI with decision cards and quick-replies
  - Live Trip Summary sidebar (destination, days, budget, vibe, cities chosen)
  - Read-only Share/Print view

- Backend (Next.js API routes or Node service)
  - Conversation endpoint orchestrating LLM + tools
  - Provider endpoints: EMT, Maps/Places/Directions, Weather
  - Itinerary generation and editing endpoints

- Database (Supabase Postgres + Auth)
  - Owns users, conversations, trips, itineraries, POIs cache, shortlists, logs

- AI Layer (OpenAI)
  - Tool calling functions with strict JSON schemas
  - Prompt templates emphasizing toddler-friendly constraints
  - Output validation and auto-retry on schema errors

## 3) Data Model (Supabase)
- users(id, email, created_at)
- profiles(user_id, home_airport, preferences_json)
- conversations(id, user_id, status, created_at)
- conversation_messages(conversation_id, role, content, tool_calls_json, tokens)
- trips(id, user_id, origin_city, destination_input, start_date, end_date, total_days, budget_mindset, pace_style, travelers_json, selected_cities_json, status)
- itineraries(id, trip_id, version, locked_sections_json, total_estimated_cost)
- itinerary_days(id, itinerary_id, day_index, city_code, weather_json)
- itinerary_activities(id, day_id, start_time, end_time, poi_id, type, tags, travel_duration_min, notes, cost_estimate_inr)
- pois(id, place_id, name, coords, city_code, tags, rating, hours_json, source)
- hotel_shortlists(id, trip_id, provider, results_json, captured_at)
- flight_shortlists(id, trip_id, provider, results_json, captured_at)
- price_snapshots(id, trip_id, type, currency, amount, source, captured_at)
- share_tokens(id, trip_id, token, expires_at)
- ai_logs(id, trip_id, prompt, response, model, latency_ms, tool_results_metadata)

## 4) Conversation Orchestrator
- State machine with slots:
  - destination_input, origin_city, dates, total_days, travelers, toddler_presence, budget_mindset, pace_style, nap_windows, accessibility, dietary
  - selected_cities, activities_selected, hotel_prefs, flight_prefs
- Policies:
  - Ask only for missing/ambiguous slots
  - Provide concise rationale for every suggestion
  - Keep "Trip Summary" up to date after each decision

### Flow Decisions
1) If destination missing → ask for destination input (country/city). Provide brief inspiration only after collecting destination.
2) After basics → propose destination cities with vibes and collect preferences.
3) Once cities chosen → fetch POIs and propose activities; build shortlist iteratively.
4) When hotel preferences provided → call EMT hotels; return 3–5 with reasons and deep links.
5) When flight preferences provided → call EMT flights; show options and cost/duration trade-offs; explicitly check cost sensitivity and adapt guidance.
6) After choices → generate itinerary with directions/weather grounding.

## 5) Provider Integrations

### 5.1 EaseMyTrip (Hotels)
- Inputs: city_code, dates, budget band, people/rooms, amenities, location preference
- Filters & scoring: price fit, kid-friendly features, proximity to selected activities, accessibility
- Output: 3–5 options with rationale and deep links

### 5.2 EaseMyTrip (Flights)
- Inputs: origin, destination, dates, passengers, cabin, stops, preferred times
- Sorting: price vs duration; expose both
- Cost sensitivity logic:
  - If option B is longer by ≤ X hours but cheaper by ≥ Y%, flag it and ask: "Are you cost sensitive?" If yes, suggest B; otherwise suggest shorter option A, especially with toddler considerations.
- Output: shortlist with fare breakdown, baggage, duration, stops, layover quality, deep links

### 5.3 Google Maps Platform
- Places: discover POIs with kid-friendly tags
- Details: ratings, opening hours
- Directions: travel time matrix for chosen activities and hotel
- Geocoding: normalize inputs

### 5.4 OpenWeatherMap
- Daily/hourly forecasts to pick indoor/outdoor and backups

## 6) AI Tool Schemas
- search_destinations({ destination_input, month, trip_days, budget_mindset, pace_style })
- propose_city_split({ candidate_cities, trip_days, toddler_profile })
- find_pois({ city_code, tags, max_results })
- get_directions({ origin, destination, mode })
- get_weather({ city_code, date })
- search_hotels({ city_code, dates, budget_band, room_count, amenities, location_pref })
- search_flights({ origin_airport, dest_airport, depart_date, return_date?, pax_json, cabin, stops_pref, time_windows })
- generate_itinerary({ cities, dates, nap_windows, poi_candidates, transit_matrix, weather, hotel_location })
- explain_rationale({ choice_type, inputs })

All return strict JSON; Zod validates responses; auto-retry on failure.

## 7) Response Composition and Rationale
- Each suggestion includes a "because" with 1–2 targeted reasons (e.g., stroller-friendly, near aquarium, short taxi rides)
- When trade-offs exist (price vs duration), articulate them and ask for a decision.

## 8) Caching, Rate Limits, and Resilience
- Cache: POIs by city+tags, Directions by origin/destination, EMT hotel/flight queries by normalized params
- Rate limiting: per-user caps, exponential backoff
- Fallbacks: serve last good snapshot with timestamp and confidence if a provider fails

## 9) Security and Privacy
- Supabase Auth; Row Level Security for user-owned data
- Secrets on server-only; never exposed to client
- Log prompts/tool outputs with PII redaction

## 10) Deployment and Observability
- ENV management for API keys
- Basic telemetry: request latency, tool call counts, LLM token usage
- Error tracking and alerting on provider failures

## 11) Acceptance Tests (Architecture)
- Conversation collects destination input and discovers places interactively
- EMT flight shortlist surfaces cost/duration trade-offs and cost sensitivity prompt
- EMT hotel shortlist returns 3–5 options with rationales and deep links
- Itinerary generation uses directions + weather and respects nap windows
- Share/Print endpoint serves read-only view


