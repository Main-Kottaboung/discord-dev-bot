import aiohttp
import os
from typing import Optional, Dict, Any


async def get_weather(location: str) -> Optional[Dict[str, Any]]:
    """
    Fetch weather data from OpenWeatherMap API.

    Args:
        location: City name or location string

    Returns:
        Dictionary containing weather data, or None if location not found

    Raises:
        Exception: If API request fails
    """
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise Exception("WEATHER_API_KEY not configured in .env")

    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": location,
            "appid": api_key,
            "units": "metric"  # Use Celsius
        }
        timeout = aiohttp.ClientTimeout(total=10)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, params=params) as response:
                # Return None if location not found
                if response.status == 404:
                    return None

                # Handle other HTTP errors
                if response.status != 200:
                    raise Exception(f"OpenWeatherMap API error: {response.status} {response.reason}")

                # Parse and return JSON
                data = await response.json()
                return data

    except aiohttp.ClientError as e:
        raise Exception(f"Network error: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to fetch weather data: {str(e)}")
