-- Trip Planner Database Schema
-- Based on the sequential workflow design

-- Cities table for destination education
CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    description TEXT,
    vibe VARCHAR(50), -- Relaxed, Sightseeing-heavy, Hybrid
    pros TEXT[],
    cons TEXT[],
    best_for TEXT[],
    ideal_days INTEGER,
    family_friendly BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Activities table for activity discovery
CREATE TABLE activities (
    id SERIAL PRIMARY KEY,
    city_id INTEGER REFERENCES cities(id),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(50), -- indoor, outdoor, cultural, adventure, family
    tags TEXT[], -- stroller-friendly, short-walk, toddler-friendly, etc.
    duration_hours DECIMAL(3,1),
    cost_usd DECIMAL(10,2),
    why_recommended TEXT,
    weather_dependent BOOLEAN DEFAULT false,
    indoor_alternative_id INTEGER REFERENCES activities(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Hotels table for hotel shortlisting
CREATE TABLE hotels (
    id SERIAL PRIMARY KEY,
    city_id INTEGER REFERENCES cities(id),
    name VARCHAR(200) NOT NULL,
    address TEXT,
    location_type VARCHAR(20), -- central, airport, beach, residential
    rating DECIMAL(2,1),
    price_usd_per_night DECIMAL(10,2),
    amenities JSONB, -- {"pool": true, "gym": false, "spa": true, "restaurant": true}
    family_features JSONB, -- {"crib": true, "kitchenette": false, "kids_pool": true}
    booking_link TEXT,
    why_recommended TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Flights table for flight shortlisting
CREATE TABLE flights (
    id SERIAL PRIMARY KEY,
    origin_city VARCHAR(100) NOT NULL,
    destination_city VARCHAR(100) NOT NULL,
    origin_code VARCHAR(3) NOT NULL,
    destination_code VARCHAR(3) NOT NULL,
    departure_time TIMESTAMP NOT NULL,
    arrival_time TIMESTAMP NOT NULL,
    duration_minutes INTEGER NOT NULL,
    stops INTEGER DEFAULT 0,
    airline VARCHAR(50) NOT NULL,
    price_usd DECIMAL(10,2) NOT NULL,
    available_seats INTEGER DEFAULT 50,
    baggage_included BOOLEAN DEFAULT true,
    why_recommended TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Weather table for itinerary planning
CREATE TABLE weather_forecasts (
    id SERIAL PRIMARY KEY,
    city_id INTEGER REFERENCES cities(id),
    forecast_date DATE NOT NULL,
    temperature_high INTEGER,
    temperature_low INTEGER,
    condition VARCHAR(50), -- sunny, rainy, cloudy, etc.
    precipitation_chance INTEGER, -- 0-100
    wind_speed INTEGER,
    recommendations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_cities_country ON cities(country);
CREATE INDEX idx_activities_city ON activities(city_id);
CREATE INDEX idx_hotels_city ON hotels(city_id);
CREATE INDEX idx_flights_route ON flights(origin_code, destination_code);
CREATE INDEX idx_flights_dates ON flights(departure_time);
CREATE INDEX idx_weather_city_date ON weather_forecasts(city_id, forecast_date);
