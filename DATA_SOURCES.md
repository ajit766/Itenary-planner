# Data Sources for AI Trip Planner MVP

This document outlines the data sources and APIs for building the AI Trip Planner application.

## Primary MVP Strategy: Consolidated API Approach

For the initial MVP, the most efficient strategy is to use a comprehensive travel API that covers multiple service types.

*   **Primary Source: EaseMyTrip API**

    The EaseMyTrip API is the designated primary choice for our MVP, especially for the Indian market. It consolidates many of our required services into a single integration point, which will significantly speed up development.

    **Services to be used from EaseMyTrip:**
    *   **Flights:** Search, pricing, availability, and booking.
    *   **Hotels:** Search, pricing, availability, and booking.
    *   **Trains:** Schedules and booking.
    *   **Buses:** Schedules and booking.
    *   **Cabs:** Inter-city taxi services.
    *   **Activities/Holidays:** Packaged tours and local experiences.

## Essential Supporting APIs

Even when using a primary travel provider, we will need to supplement it with other essential services.

*   **Maps & Geolocation: Google Maps Platform**
    *   **Reason:** Unmatched for displaying maps, finding points of interest (restaurants, ATMs, etc.), calculating routes, and converting addresses to coordinates. This is critical for building the itinerary visually.
    *   **Specific APIs to be used:**
        *   **Maps SDK:** To display interactive maps.
        *   **Places API:** To find detailed information on millions of places (restaurants, attractions, etc.) and their reviews.
        *   **Directions API:** For calculating travel times and routes between points in the itinerary.
        *   **Geocoding API:** To convert addresses into geographic coordinates.

*   **Real-time Weather: OpenWeatherMap API**
    *   **Reason:** Essential for the "smart adjustments" feature. It's reliable, easy to use, and has a suitable free tier for an MVP.

## Alternative & Future Expansion Sources

As the application grows, we can incorporate these additional sources to increase our inventory, improve pricing, or add new features.

*   **Accommodation:**
    *   Booking.com API
    *   Expedia (Rapid API)
    *   Hotelbeds

*   **Flights:**
    *   Skyscanner API
    *   Amadeus / Sabre (for global scale)

*   **Activities & Tours:**
    *   Viator
    *   GetYourGuide
    *   Klook

*   **Local Events (India):**
    *   BookMyShow
    *   Paytm Insider