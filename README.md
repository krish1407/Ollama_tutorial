# Weather & News Search Application

A Streamlit application that fetches weather and top 5 news headlines for any country/region.

## Setup Instructions

### 1. Get API Keys

- **OpenWeatherMap API Key**: https://openweathermap.org/api
- **NewsAPI Key**: https://newsapi.org/

### 2. Configure API Keys (Choose one method)

#### Method 1: Environment Variables (Recommended)

```bash
# Set environment variables
export OPENWEATHER_API_KEY='your_openweathermap_key_here'
export NEWSAPI_KEY='your_newsapi_key_here'

# Run the application
streamlit run news_websearch.py
```

#### Method 2: Using .env File

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your actual API keys
# Then run:
streamlit run news_websearch.py
```

### 3. Run the Application

```bash
streamlit run news_websearch.py
```

## Features

- 🔍 Search by country/region name
- 🌤️ Current weather information (temperature, humidity, wind, etc.)
- 📰 Top 5 news headlines
- 🔒 Secure API key management using environment variables

## Security Notes

- API keys are stored in environment variables, not hardcoded
- Never commit your `.env` file to version control
- Use `.env.example` as a template only

## Requirements

- Python 3.7+
- Streamlit
- requests

## Installation

```bash
pip install streamlit requests
```

## Usage

1. Set your API keys as environment variables or in a `.env` file
2. Run `streamlit run news_websearch.py`
3. Enter a country/region name in the search box
4. View weather and news results
