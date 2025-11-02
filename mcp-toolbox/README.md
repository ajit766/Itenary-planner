# 🌍 MCP Toolbox — Trip Planner Toolset

This repository defines a **Multi-Component Protocol (MCP)** toolbox for the **Trip Planner AI** project.  
It integrates multiple public APIs (Open-Meteo, GeoDB Cities, Google Places, GetYourGuide, Wikipedia, and Google Custom Search Engine)  
to provide complete travel intelligence — from city discovery to weather forecasts.

---

## 🧰 Overview

### File
- `tools.yaml` — main definition file for all MCP sources and tools.
- `README.md` — this file (usage and configuration guide).

### Components
| Category | API | Purpose |
|-----------|------|----------|
| Weather | **Open-Meteo** | 7-day forecasts and temperature trends |
| Geocoding | **Open-Meteo Geocoding** | Convert city names to coordinates |
| Cities | **GeoDB Cities (RapidAPI)** | Fetch top populated cities by country |
| Places | **Google Places API** | Hotel and lodging search by city or name |
| Activities | **GetYourGuide (RapidAPI)** | Fetch family/kid-friendly local activities |
| Knowledge | **Wikipedia API** | City summaries and highlights |
| Search | **Google Custom Search Engine (CSE)** | SERP-based search for flights, hotels, or transit |

---

## ⚙️ Environment Variables

Create a `.env` file in the same directory as `tools.yaml`:

```bash
RAPIDAPI_KEY=your_rapidapi_key
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
GOOGLE_CSE_KEY=your_google_cse_key
GOOGLE_CSE_CX=your_custom_search_engine_id
