# Trip Planner MVP — Conversation-First Requirements

## 1) Scope and Persona
- Persona: Indian couple + 2-year-old child, international travel for vacation (initial focus)
- Trip length: 5–7 days (user-provided)
- Destination: Provided by user as an input; places to visit are discovered collaboratively during the conversation
- Budget mindset: Frugal / Moderate / Premium (value-focused defaults)
- Travel vibe: Relaxed vs Sightseeing-heavy vs Hybrid

## 2) Conversational UX (End-to-End)
Goal: The AI conducts a guided conversation, educates with context, gathers constraints, then co-creates an itinerary with hotel and flight options from EaseMyTrip (EMT).

### 2.1 Stages and Sample Prompts
- Stage A: Trip Basics
  - Ask: origin city/airport, destination country/city (user input), dates and total days, travelers and ages, budget mindset, pace style.
  - Confirm: nap windows, stroller and accessibility needs, dietary preferences.

- Stage B: Educate and Inspire (Discovery of places happens here)
  - Present popular cities within the selected destination with concise "vibes" and pros/cons tailored for a toddler.
  - Provide links and 1–2 short videos per city for deeper understanding.
  - Ask which cities resonate; user can pick or ask for alternatives.

- Stage C: Destination Split and Feasibility
  - Propose 1–2 city splits for the given duration (e.g., 3N Bangkok + 3N Phuket), with rationale.
  - Validate transit times and practicality for a toddler.

- Stage D: Activities and Experiences (Discovery continues)
  - Suggest kid-friendly activities per chosen city with tags (indoor, shaded, short-walk, stroller-friendly) and "why" notes.
  - Offer backups for weather or nap conflicts.
  - User accepts/declines; AI refines the set.

- Stage E: Hotel Shortlisting (EMT)
  - Ask: location preference (central/airport/beach), room types, must-haves (crib, kitchenette).
  - Query EMT; present 3–5 hotels with price, location, ratings, family notes, distances to selected activities, cancellation policy, and deep links.
  - Explain "why shortlisted" for each.

- Stage F: Flights Shortlisting and Cost Sensitivity (EMT)
  - Ask: preferred departure window, number of stops, baggage needs.
  - Query EMT for flights; present options with duration, stops, layovers, and total fare.
  - Cost sensitivity guidance: If a longer flight is slightly cheaper, explicitly call it out and ask if the user is cost sensitive. Offer recommendations accordingly (e.g., choose shorter flight with toddler unless price gap is significant).
  - Allow user to sort by price or duration; support follow-up filters (non-stop only, specific airline).

- Stage G: Day-by-Day Itinerary
  - Compose a schedule for each day (morning/afternoon/evening) respecting nap windows, walking caps, opening hours, weather, and chosen activities/hotel locations.
  - Provide travel times between items and rain-safe alternates.
  - Allow scoped edits (swap activity, nudge time, regenerate a day) and keep a visible trip summary.

- Stage H: Cost Overview and Actions
  - Cost roll-up: hotels (from EMT), flights (from EMT), transport, activities, meals buffer; show source and confidence.
  - Actions: deep-link to book flights and hotels on EMT; generate shareable link; printable/PDF view.

## 3) Functional Requirements
- Conversation engine that:
  - Maintains structured state (slots): destination, dates, travelers, budget, vibe, nap windows, selected cities, activities, hotel and flight preferences.
  - Detects missing information and asks targeted follow-up questions.
  - Surfaces suggestions with rationales, links, and optional videos.
  - Performs EMT hotel and flight searches, then renders shortlists with explanations and deep links.
  - Generates and updates an itinerary using grounded data (POIs, directions, weather) and user decisions.

- Hotel search (EMT): filters by budget band, family amenities, location; returns 3–5 options with reasons and deep links.
- Flight search (EMT): presents options, highlights price-vs-duration trade-offs, asks about cost sensitivity, and adapts recommendations accordingly.
- Itinerary generation: day-by-day blocks, travel times, nap blocks, backups; supports scoped edits.
- Cost estimation: per-day and total estimates with sources; allow currency display in INR by default.
- Shareable read-only view and printable layout.

## 4) Non-Functional Requirements
- Performance: 3–6s typical responses when cached; 6–12s when aggregating providers.
- Reliability: clear fallbacks and confidence labels when providers or quotas fail.
- Observability: log Gemini prompts/responses and provider calls (redact PII); leverage Vertex AI/ADK tracing.
- Accessibility: keyboard, contrast, large tap targets.
- Privacy: store minimal PII, secure keys, comply with providers' ToS.

## 5) Data Sources
- EaseMyTrip: hotels and flights (search, pricing, availability, deep links/booking flow)
- Google Maps Platform: Places, Details, Directions, Geocoding
- OpenWeatherMap: daily/hourly forecasts for scheduling
- Google Gemini (Vertex AI) via Google AI Developer Kit (ADK): reasoning and itinerary composition with validated JSON outputs

## 6) Acceptance Criteria (MVP)
- Destination is collected as an explicit input.
- Conversation captures days, travelers/ages, budget mindset, travel vibe, nap windows.
- AI educates on cities within the destination and discovers places/activities collaboratively.
- EMT hotel shortlist: 3–5 options with rationale and deep links.
- EMT flight shortlist: options with duration/price trade-offs; cost sensitivity check and tailored guidance.
- Generated itinerary: day-by-day plan with travel times, weather notes, and backups.
- Cost overview with sources and confidence.
- Shareable link and printable PDF available.


