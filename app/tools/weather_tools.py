from app.models import QueryState, LocationInformation
from app.agents import location_extractor_agent
import requests
from app.config import settings
import random
from datetime import datetime

MOCK_RESPONSE_TEMPLATE = """
🌤️ Weather Report for {location_display}
📅 Generated at: {current_time} (Mock Data)

🌡️ Temperature: {temp}°C
☁️ Condition: {condition}
💧 Humidity: {humidity}%
💨 Wind Speed: {wind_speed} km/h
📊 Pressure: {pressure} hPa

Note: This is mock data generated because the OpenWeatherMap API key is not configured. For real weather data, please set up your API key in the environment variables.
"""

async def extract_location(query: str) -> LocationInformation:
    """Extract location information from user query."""
    resp = await location_extractor_agent.run(query)
    return resp.data

def get_mock_weather_response(location_information: LocationInformation) -> str:
    """Generate a realistic mock weather response when API key is not available."""
    city = location_information.city or "Unknown City"
    state = location_information.state_code or ""
    country = location_information.country_code or ""
    
    # Mock weather conditions
    conditions = [
        "sunny", "partly cloudy", "cloudy", "rainy", "snowy", "foggy", "clear"
    ]
    condition = random.choice(conditions)
    
    # Mock temperature (in Celsius)
    temp = random.randint(-10, 35)
    
    # Mock humidity
    humidity = random.randint(30, 90)
    
    # Mock wind speed (km/h)
    wind_speed = random.randint(0, 25)
    
    # Mock pressure (hPa)
    pressure = random.randint(980, 1030)
    
    # Current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    location_display = f"{city}"
    if state:
        location_display += f", {state}"
    if country:
        location_display += f", {country}"
    
    mock_response = MOCK_RESPONSE_TEMPLATE.format(
        location_display=location_display,
        current_time=current_time,
        temp=temp,
        condition=condition,
        humidity=humidity,
        wind_speed=wind_speed,
        pressure=pressure
    )
    return mock_response


async def weather_tool(state: QueryState) -> QueryState:
    """Process weather-related queries."""
    location_information: LocationInformation = await extract_location(query=state.query)
    
    # Get OpenWeatherMap API key from environment
    api_key = settings.openweather_api_key
    if not api_key:
        # Use mock response when API key is not configured
        mock_weather = get_mock_weather_response(location_information)
        state.location_information = location_information
        state.result = mock_weather
        return state
    
    try:
        # Step 1: Geocoding API call to get coordinates
        geocode_url = "http://api.openweathermap.org/geo/1.0/direct"
        geocode_params = {
            'q': ','.join([x for x in [
                location_information.city, 
                location_information.state_code, 
                location_information.country_code
            ] if x]),
            'limit': 1,
            'appid': api_key
        }
        
        geocode_response = requests.get(geocode_url, params=geocode_params)
        geocode_response.raise_for_status()
        geocode_data = geocode_response.json()
        
        if not geocode_data:
            state.result = f"Location '{location_information.city}' not found"
            return state
        
        # Get coordinates from first result
        location = geocode_data[0]
        lat = location['lat']
        lon = location['lon']
        
        # Step 2: Weather API call to get weather data
        weather_url = "https://api.openweathermap.org/data/3.0/onecall/overview"
        weather_params = {
            'lon': lon,
            'lat': lat,
            'appid': api_key
        }
        
        weather_response = requests.get(weather_url, params=weather_params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        # Extract weather overview
        weather_overview = weather_data.get('weather_overview', 'Weather information not available')
        
        state.location_information = location_information
        state.result = weather_overview
        
    except requests.exceptions.RequestException as e:
        state.result = f"Error fetching weather data: {e}"
    except Exception as e:
        state.result = f"Error processing weather request: {e}"
    
    return state 