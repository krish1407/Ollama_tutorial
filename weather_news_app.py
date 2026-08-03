import streamlit as st
import requests
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Get API keys
weather_api_key = os.getenv("OPENWEATHER_API_KEY", "")
news_api_key = os.getenv("NEWSAPI_KEY", "")

# Check if API keys are configured
if not weather_api_key or not news_api_key:
    st.error("❌ API keys not configured")
    st.warning("Please create a .env file with your API keys:")
    st.code("OPENWEATHER_API_KEY=your_openweathermap_key_here\nNEWSAPI_KEY=your_newsapi_key_here", language="bash")
    st.info("1. Copy .env.example to .env\n2. Edit .env with your keys\n3. Run the app")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Weather & News Search",
    page_icon="🌤️📰",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .weather-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .news-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 4px solid #4CAF50;
    }
    .header-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
    }
    .input-container {
        background-color: #e8f4f8;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .error-message {
        background-color: #ffebee;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #f44336;
    }
    .success-message {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="header-title">🌤️📰 Weather & News Search</div>', unsafe_allow_html=True)

# Input section
st.markdown('<div class="input-container">', unsafe_allow_html=True)
st.header("📍 Enter Location")
st.markdown("**Format:** `City, Country` (e.g., `New Jersey, USA` or `London, UK`)")

# Input for city and country
location_input = st.text_input(
    "Enter location (City, Country):",
    placeholder="e.g., New Jersey, USA",
    key="location_input"
)

# Button to fetch data
if st.button("🔍 Get Weather & News", type="primary", use_container_width=True):
    if location_input:
        # Parse the input
        try:
            parts = location_input.split(",")
            if len(parts) >= 2:
                city = parts[0].strip()
                country = parts[1].strip()
            else:
                st.error("❌ Please enter location in format: City, Country")
                st.stop()
            
            # Fetch weather data
            st.info("📡 Fetching weather data...")
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
                
                # Sunrise and sunset
                sunrise = weather_data['sys']['sunrise']
                sunset = weather_data['sys']['sunset']
                
                # Display weather information
                st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                st.markdown(f"**📍 Location:** {location}")
                st.markdown(f"**🌡️ Temperature:** {temp}°C")
                st.markdown(f"**💨 Feels Like:** {feels_like}°C")
                st.markdown(f"**🌦️ Condition:** {condition}")
                st.markdown("---")
                st.markdown("**📊 Details:**")
                st.markdown(f"- **Humidity:** {humidity}%")
                st.markdown(f"- **Wind Speed:** {wind_speed} m/s")
                st.markdown(f"- **Pressure:** {pressure} hPa")
                st.markdown(f"- **Visibility:** {visibility} m")
                st.markdown("---")
                st.markdown(f"**🌅 Sunrise:** {datetime.fromtimestamp(sunrise).strftime('%Y-%m-%d %H:%M:%S')}")
                st.markdown(f"**🌇 Sunset:** {datetime.fromtimestamp(sunset).strftime('%Y-%m-%d %H:%M:%S')}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Fetch news data
                st.info("📡 Fetching news data...")
                # Convert country name to ISO code if needed
                country_codes = {
                    'usa': 'us', 'united states': 'us', 'america': 'us',
                    'uk': 'gb', 'united kingdom': 'gb', 'britain': 'gb',
                    'canada': 'ca', 'australia': 'au', 'india': 'in',
                    'japan': 'jp', 'china': 'cn', 'germany': 'de', 'france': 'fr'
                }
                
                country_lower = country.lower()
                if country_lower in country_codes:
                    iso_code = country_codes[country_lower]
                else:
                    # Try to use as-is or default to us
                    iso_code = country if country in ['us', 'gb', 'ca', 'au', 'in', 'jp', 'cn', 'de', 'fr'] else 'us'
                
                news_url = f"https://newsapi.org/v2/top-headlines?country={iso_code}&apiKey={news_api_key}"
                news_response = requests.get(news_url, timeout=10)
                
                if news_response.status_code == 200:
                    news_data = news_response.json()
                    articles = news_data.get('articles', [])
                    
                    # Display news headlines
                    st.markdown('<div class="news-card">', unsafe_allow_html=True)
                    st.markdown(f"**📰 TOP 5 NEWS HEADLINES FROM {country.upper()}**")
                    st.markdown("---")
                    
                    if articles:
                        for i, article in enumerate(articles[:5], 1):
                            title = article.get('title', 'No Title')
                            description = article.get('description', 'No description')
                            url = article.get('url', '#')
                            source = article.get('source', {}).get('name', 'Unknown')
                            published_at = article.get('publishedAt', '')
                            
                            st.markdown(f"**{i}. {title}**")
                            if description:
                                st.markdown(f"*{description[:150]}...*")
                            st.markdown(f"📰 {source} | 🕒 {published_at[:10] if published_at else 'Unknown'}")
                            if url and url != '#':
                                st.markdown(f"[Read more]({url})")
                            st.markdown("---")
                    else:
                        st.warning("⚠️ No news articles found for this region")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error(f"❌ News API Error: {news_response.status_code}")
                    st.write(f"Response: {news_response.text[:200]}")
                    
            else:
                st.error(f"❌ Weather API Error: {weather_response.status_code}")
                st.write(f"Response: {weather_response.text[:200]}")
                
        except Exception as e:
            st.error(f"❌ Error processing location: {str(e)}")
            st.write("Please check your input format (City, Country)")
    else:
        st.warning("⚠️ Please enter a location")
else:
    # Show placeholder
    st.markdown('<div class="weather-card">', unsafe_allow_html=True)
    st.markdown("**🌤️ Enter a location above to get weather and news!**")
    st.markdown("**Example:** `New Jersey, USA` or `London, UK`")
    st.markdown('</div>', unsafe_allow_html=True)
