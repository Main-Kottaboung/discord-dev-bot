import asyncio
from dotenv import load_dotenv
from services.weather_service import get_weather
import os

load_dotenv()

async def main():
    try:
        data = await get_weather("London")
        if data is None:
            print("Location not found")
            return
        # print a few fields
        print("City:", data.get('name'))
        print("Weather:", data.get('weather'))
        print("Main:", data.get('main'))
    except Exception as e:
        print('ERROR:', e)

asyncio.run(main())
