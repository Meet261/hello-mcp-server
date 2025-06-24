import requests
from bs4 import BeautifulSoup
import os

def search_web(query: str, num_results: int = 5) -> str:
    """Search the web using a search API"""
    # Example using DuckDuckGo or other search APIs
    try:
        # This is a simplified example - you'd use a real search API
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1"
        response = requests.get(url)
        data = response.json()
        
        results = []
        for item in data.get('RelatedTopics', [])[:num_results]:
            if 'Text' in item and 'FirstURL' in item:
                results.append(f"• {item['Text']}\n  URL: {item['FirstURL']}")
        
        return "\n\n".join(results) if results else "No results found"
    except Exception as e:
        return f"Search failed: {str(e)}"

def scrape_webpage(url: str) -> str:
    """Extract text content from a webpage"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; MCP-Server/1.0)'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Limit length
        return text[:5000] + "..." if len(text) > 5000 else text
        
    except Exception as e:
        return f"Failed to scrape webpage: {str(e)}"

def get_weather(location: str) -> str:
    """Get weather information for a location"""
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "Weather API key not configured"
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            weather = data['weather'][0]['description']
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            
            return f"Weather in {location}:\n• {weather.title()}\n• Temperature: {temp}°C (feels like {feels_like}°C)\n• Humidity: {humidity}%"
        else:
            return f"Weather data not found for {location}"
            
    except Exception as e:
        return f"Weather lookup failed: {str(e)}"