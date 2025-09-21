-- Sample data for Trip Planner
-- Based on the sequential workflow design

-- Insert cities (Step 2: Destination Education)
INSERT INTO cities (name, country, description, vibe, pros, cons, best_for, ideal_days, family_friendly) VALUES
('Bangkok', 'Thailand', 'Vibrant capital with rich culture and modern amenities', 'Hybrid', 
 ARRAY['Great food scene', 'Rich cultural sites', 'Excellent shopping', 'Family-friendly attractions'],
 ARRAY['Hot and humid', 'Busy traffic', 'Language barrier'],
 ARRAY['Culture', 'Food', 'Shopping', 'Family activities'], 4, true),

('Phuket', 'Thailand', 'Beautiful island with stunning beaches and resorts', 'Relaxed',
 ARRAY['Beautiful beaches', 'Water activities', 'Luxury resorts', 'Relaxing atmosphere'],
 ARRAY['More expensive', 'Touristy areas', 'Limited cultural sites'],
 ARRAY['Beach time', 'Relaxation', 'Water sports'], 3, true),

('Chiang Mai', 'Thailand', 'Cultural hub in northern Thailand with temples and mountains', 'Sightseeing-heavy',
 ARRAY['Rich cultural heritage', 'Cooler climate', 'Mountain activities', 'Authentic experiences'],
 ARRAY['Limited beach access', 'More walking required', 'Fewer luxury options'],
 ARRAY['Culture', 'Temples', 'Nature', 'Authentic experiences'], 3, true),

('Tokyo', 'Japan', 'Modern metropolis blending tradition and innovation', 'Hybrid',
 ARRAY['Safe and clean', 'Excellent public transport', 'Unique experiences', 'Great food'],
 ARRAY['Expensive', 'Language barrier', 'Crowded'],
 ARRAY['Culture', 'Technology', 'Food', 'Shopping'], 5, true),

('Kyoto', 'Japan', 'Ancient capital with temples, gardens, and traditional culture', 'Sightseeing-heavy',
 ARRAY['Rich history', 'Beautiful temples', 'Traditional experiences', 'Photogenic'],
 ARRAY['Lots of walking', 'Crowded during peak season', 'Limited nightlife'],
 ARRAY['Culture', 'History', 'Temples', 'Photography'], 4, true),

('Paris', 'France', 'City of Light with iconic landmarks and world-class cuisine', 'Hybrid',
 ARRAY['Iconic landmarks', 'World-class museums', 'Excellent food', 'Romantic atmosphere'],
 ARRAY['Expensive', 'Language barrier', 'Crowded tourist areas'],
 ARRAY['Culture', 'Art', 'Food', 'Romance'], 5, true),

('Barcelona', 'Spain', 'Vibrant city with unique architecture and Mediterranean charm', 'Hybrid',
 ARRAY['Unique architecture', 'Great food scene', 'Beach access', 'Vibrant culture'],
 ARRAY['Pickpocketing concerns', 'Language barrier', 'Crowded in summer'],
 ARRAY['Architecture', 'Food', 'Beach', 'Culture'], 4, true);

-- Insert activities (Step 4: Activity Discovery)
INSERT INTO activities (city_id, name, description, category, tags, duration_hours, cost_usd, why_recommended, weather_dependent) VALUES
-- Bangkok activities
(1, 'Chatuchak Weekend Market', 'World''s largest weekend market with food, shopping, and entertainment', 'cultural', 
 ARRAY['indoor', 'stroller-friendly', 'short-walk', 'toddler-friendly'], 3.0, 0.0, 
 'Perfect for families with toddlers - lots to see, food options, and stroller-friendly', false),

(1, 'Siam Ocean World', 'Large aquarium with marine life exhibits and interactive shows', 'family',
 ARRAY['indoor', 'stroller-friendly', 'toddler-friendly', 'air-conditioned'], 2.5, 25.0,
 'Great for 2-year-olds - air-conditioned, educational, and engaging', false),

(1, 'Wat Pho Temple', 'Famous temple with the reclining Buddha statue', 'cultural',
 ARRAY['outdoor', 'short-walk', 'cultural'], 1.5, 3.0,
 'Iconic cultural site, but may be challenging with stroller due to steps', true),

(1, 'Lumpini Park', 'Large public park with playgrounds and paddle boats', 'outdoor',
 ARRAY['outdoor', 'stroller-friendly', 'toddler-friendly', 'playground'], 2.0, 0.0,
 'Perfect for toddlers to run around and play, with playground facilities', true),

-- Phuket activities
(2, 'Patong Beach', 'Famous beach with water activities and family-friendly areas', 'outdoor',
 ARRAY['outdoor', 'beach', 'water-activities'], 4.0, 0.0,
 'Great beach for families, but bring sun protection for toddlers', true),

(2, 'Phuket Aquarium', 'Marine life center with touch tanks and shows', 'family',
 ARRAY['indoor', 'stroller-friendly', 'toddler-friendly'], 2.0, 15.0,
 'Educational and fun for young children, air-conditioned', false),

(2, 'Big Buddha Phuket', 'Large Buddha statue with panoramic views', 'cultural',
 ARRAY['outdoor', 'cultural', 'viewpoint'], 1.5, 0.0,
 'Beautiful views and cultural significance, but may require carrying toddler', true),

-- Tokyo activities
(4, 'Tokyo Disneyland', 'Magical theme park with Disney characters and rides', 'family',
 ARRAY['indoor', 'outdoor', 'stroller-friendly', 'toddler-friendly'], 8.0, 80.0,
 'Perfect for families with young children, lots of toddler-friendly attractions', true),

(4, 'Ueno Zoo', 'Large zoo with pandas and family-friendly exhibits', 'family',
 ARRAY['outdoor', 'stroller-friendly', 'toddler-friendly'], 3.0, 5.0,
 'Great for toddlers to see animals, stroller-friendly paths', true),

(4, 'Senso-ji Temple', 'Ancient Buddhist temple in Asakusa', 'cultural',
 ARRAY['outdoor', 'cultural', 'short-walk'], 1.5, 0.0,
 'Important cultural site, but may be crowded with stroller', true);

-- Insert hotels (Step 5: Hotel Shortlisting)
INSERT INTO hotels (city_id, name, address, location_type, rating, price_usd_per_night, amenities, family_features, why_recommended) VALUES
-- Bangkok hotels
(1, 'Hilton Bangkok', '1031 Wireless Road, Lumpini, Bangkok 10330', 'central', 4.5, 120.0,
 '{"pool": true, "gym": true, "spa": true, "restaurant": true, "wifi": true}',
 '{"crib": true, "kitchenette": false, "kids_pool": true, "babysitting": true}',
 'Perfect location near Chatuchak Market, excellent family amenities'),

(1, 'Novotel Bangkok Siam Square', '392/44 Siam Square Soi 6, Rama I Rd, Bangkok 10330', 'central', 4.2, 95.0,
 '{"pool": true, "gym": false, "spa": false, "restaurant": true, "wifi": true}',
 '{"crib": true, "kitchenette": true, "kids_pool": false, "babysitting": false}',
 'Great value, close to Siam Ocean World, connecting rooms available'),

(1, 'Grand Hyatt Erawan Bangkok', '494 Rajdamri Road, Bangkok 10330', 'central', 4.7, 180.0,
 '{"pool": true, "gym": true, "spa": true, "restaurant": true, "wifi": true}',
 '{"crib": true, "kitchenette": false, "kids_pool": true, "babysitting": true}',
 'Luxury option with excellent family services and central location'),

-- Phuket hotels
(2, 'JW Marriott Phuket Resort & Spa', '231 Moo 3, Mai Khao, Phuket 83110', 'beach', 4.6, 200.0,
 '{"pool": true, "gym": true, "spa": true, "restaurant": true, "wifi": true}',
 '{"crib": true, "kitchenette": false, "kids_pool": true, "babysitting": true}',
 'Beachfront luxury resort with excellent family facilities'),

(2, 'Holiday Inn Resort Phuket', '52 Thaweewong Road, Patong Beach, Phuket 83150', 'beach', 4.3, 140.0,
 '{"pool": true, "gym": false, "spa": true, "restaurant": true, "wifi": true}',
 '{"crib": true, "kitchenette": true, "kids_pool": true, "babysitting": false}',
 'Great beach location, family-friendly with kids club'),

-- Tokyo hotels
(4, 'Park Hyatt Tokyo', '3-7-1-2 Nishi-Shinjuku, Shinjuku, Tokyo 160-0023', 'central', 4.8, 400.0,
 '{"pool": true, "gym": true, "spa": true, "restaurant": true, "wifi": true}',
 '{"crib": true, "kitchenette": false, "kids_pool": false, "babysitting": true}',
 'Luxury option with excellent service, close to major attractions'),

(4, 'Hilton Tokyo', '6-6-2 Nishi-Shinjuku, Shinjuku, Tokyo 160-0023', 'central', 4.4, 180.0,
 '{"pool": true, "gym": true, "spa": true, "restaurant": true, "wifi": true}',
 '{"crib": true, "kitchenette": false, "kids_pool": true, "babysitting": true}',
 'Great location, family-friendly with connecting rooms available');

-- Insert flights (Step 6: Flight Shortlisting)
INSERT INTO flights (origin_city, destination_city, origin_code, destination_code, departure_time, arrival_time, duration_minutes, stops, airline, price_usd, available_seats, baggage_included, why_recommended) VALUES
-- Mumbai to Bangkok
('Mumbai', 'Bangkok', 'BOM', 'BKK', '2024-04-20 10:30:00', '2024-04-20 15:00:00', 270, 0, 'Thai Airways', 450.0, 25, true, 'Perfect timing for toddler, non-stop flight, excellent service'),
('Mumbai', 'Bangkok', 'BOM', 'BKK', '2024-04-20 08:00:00', '2024-04-20 16:15:00', 375, 1, 'Air India', 380.0, 15, true, '15% cheaper but longer with stop in Delhi'),
('Mumbai', 'Bangkok', 'BOM', 'BKK', '2024-04-20 14:00:00', '2024-04-20 20:30:00', 270, 0, 'IndiGo', 420.0, 30, true, 'Good value non-stop, afternoon departure'),

-- Bangkok to Phuket
('Bangkok', 'Phuket', 'BKK', 'HKT', '2024-04-23 09:00:00', '2024-04-23 10:30:00', 90, 0, 'Thai Airways', 120.0, 40, true, 'Short domestic flight, perfect for toddler'),
('Bangkok', 'Phuket', 'BKK', 'HKT', '2024-04-23 15:00:00', '2024-04-23 16:30:00', 90, 0, 'Bangkok Airways', 110.0, 35, true, 'Afternoon departure, good value'),

-- Mumbai to Tokyo
('Mumbai', 'Tokyo', 'BOM', 'NRT', '2024-04-20 11:00:00', '2024-04-20 22:30:00', 690, 0, 'Japan Airlines', 650.0, 20, true, 'Non-stop to Tokyo, excellent service for families'),
('Mumbai', 'Tokyo', 'BOM', 'NRT', '2024-04-20 08:30:00', '2024-04-20 23:45:00', 675, 1, 'Air India', 580.0, 18, true, 'Cheaper with stop in Delhi, longer journey'),

-- Mumbai to Paris
('Mumbai', 'Paris', 'BOM', 'CDG', '2024-04-20 13:00:00', '2024-04-20 19:30:00', 390, 0, 'Air France', 750.0, 12, true, 'Non-stop to Paris, excellent for families'),
('Mumbai', 'Paris', 'BOM', 'CDG', '2024-04-20 10:00:00', '2024-04-20 22:15:00', 495, 1, 'Lufthansa', 680.0, 15, true, 'Stop in Frankfurt, good value option');

-- Insert weather forecasts (Step 7: Itinerary Generation)
INSERT INTO weather_forecasts (city_id, forecast_date, temperature_high, temperature_low, condition, precipitation_chance, wind_speed, recommendations) VALUES
-- Bangkok weather
(1, '2024-04-20', 35, 28, 'sunny', 20, 10, 'Hot and humid - bring sun protection and stay hydrated'),
(1, '2024-04-21', 34, 27, 'partly_cloudy', 30, 12, 'Slightly cooler, good for outdoor activities'),
(1, '2024-04-22', 33, 26, 'rainy', 80, 15, 'Rain expected - plan indoor activities like Siam Ocean World'),

-- Phuket weather
(2, '2024-04-23', 32, 26, 'sunny', 15, 8, 'Perfect beach weather - ideal for water activities'),
(2, '2024-04-24', 31, 25, 'partly_cloudy', 25, 10, 'Good weather for beach and outdoor activities'),
(2, '2024-04-25', 30, 24, 'sunny', 10, 6, 'Excellent beach conditions'),

-- Tokyo weather
(4, '2024-04-20', 18, 12, 'sunny', 10, 8, 'Pleasant spring weather - perfect for outdoor activities'),
(4, '2024-04-21', 20, 14, 'partly_cloudy', 20, 10, 'Good weather for sightseeing'),
(4, '2024-04-22', 22, 16, 'sunny', 5, 6, 'Beautiful spring day - ideal for parks and outdoor activities');
