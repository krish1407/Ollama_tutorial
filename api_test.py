import requests
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Get API keys
weather_api_key = os.getenv("OPENWEATHER_API_KEY", "")
news_api_key = os.getenv("NEWSAPI_KEY", "")
try:
    if not weather_api_key or not news_api_key:
        print("API keys not found in .env file")
        print("Please ensure both OPENWEATHER_API_KEY and NEWSAPI_KEY are set")
        exit(1)

    # Query for New Jersey
    city = "New Jersey"
    city_lower = city.lower().replace(" ", "")

    print("=" * 60)
    print(" WEATHER & NEWS FOR NEW JERSEY")
    print("=" * 60)

    # Fetch weather data
    print("\n Fetching weather data...")
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric&lang=en"
    weather_response = requests.get(weather_url, timeout=10)

    if weather_response.status_code == 200:
        weather_data = weather_response.json()
        
        # Extract weather information
        location = f"{weather_data['name']}, {weather_data['sys']['country']}"
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        condition = weather_data['weather'][0]['description'].capitalize()
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        pressure = weather_data['main']['pressure']
        visibility = weather_data['visibility']
        
        print(f"\n {location}")
        print(f" Temperature: {temp}°C")
        print(f" Feels Like: {feels_like}°C")
        print(f" Condition: {condition}")
        print(f"\n Details:")
        print(f"  Humidity: {humidity}%")
        print(f"  Wind Speed: {wind_speed} m/s")
        print(f"  Pressure: {pressure} hPa")
        print(f"  Visibility: {visibility} m")
        
        # Sunrise and sunset
        sunrise = weather_data['sys']['sunrise']
        sunset = weather_data['sys']['sunset']
        print(f"\nSunrise: {datetime.fromtimestamp(sunrise).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Sunset: {datetime.fromtimestamp(sunset).strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Fetch news data
        print("\n Fetching news data...")
        news_url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}"
        news_response = requests.get(news_url, timeout=10)
        
        if news_response.status_code == 200:
            news_data = news_response.json()
            articles = news_data.get('articles', [])
            
            print(f"\n TOP 5 NEWS HEADLINES")
            print("=" * 60)
            
            for i, article in enumerate(articles[:5], 1):
                title = article.get('title', 'No Title')
                description = article.get('description', 'No description')
                url = article.get('url', '#')
                source = article.get('source', {}).get('name', 'Unknown')
                published_at = article.get('publishedAt', '')
                
                print(f"\n{i}. {title}")
                if description:
                    print(f"   {description[:150]}...")
                print(f"    {source} | {published_at[:10] if published_at else 'Unknown'}")
                if url and url != '#':
                    print(f"   {url}")
            
            print("\n" + "=" * 60)
            
        else:
            print(f"\n News API Error: {news_response.status_code}")
            print(f"Response: {news_response.text[:200]}")        

except requests.exceptions.RequestException as e:
    print(f"\n Error fetching data: {str(e)}")

