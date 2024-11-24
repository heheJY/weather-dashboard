from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime
import pytz

app = Flask(__name__)

# API Keys
IPSTACK_API_KEY = "IPSTACK_API_KEY"
OPENWEATHER_API_KEY = "OPENWEATHER_API_KEY"
NEWS_API_KEY = "NEWS_API_KEY"

def get_recommendations(weather, pollution):
    recommendations = []

    # Weather-based recommendations
    if "rain" in weather.get("Weather", "").lower():
        recommendations.append("It's raining. Don't forget to bring an umbrella!")
    elif weather.get("Temperature", 0) > 30:
        recommendations.append("It's hot outside. Drink plenty of water and stay hydrated!")
    elif weather.get("Temperature", 0) < 15:
        recommendations.append("It's cold outside. Wear warm clothes!")

    if weather.get("Humidity", 0) > 80:
        recommendations.append("High humidity detected. Stay in cool areas if possible.")

    # Pollution-based recommendations
    if pollution.get("AQI", 0) >= 4:
        recommendations.append("The air quality is poor. Consider wearing a mask outdoors.")
    elif pollution.get("AQI", 0) == 3:
        recommendations.append("Moderate air quality. Sensitive groups should limit outdoor activities.")

    if not recommendations:
        recommendations.append("Weather looks great today! Enjoy your day.")

    return recommendations

# Function to fetch weather-related news
def get_weather_news(city, country):
    if not city or not country:
        city = "global"  # Fallback if location is unavailable

    # Search for news using city, country, and weather context
    query = f"weather {city} {country}"
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&pageSize=5&apiKey={NEWS_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return [
            {"title": article["title"], "url": article["url"], "source": article["source"]["name"]}
            for article in articles
        ]
    else:
        return [{"Error": "Unable to fetch news"}]

# Function to get geolocation from IP
def get_geolocation(ip):
    url = f"http://api.ipstack.com/{ip}?access_key={IPSTACK_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "IP": data.get("ip"),
            "City": data.get("city"),
            "Region": data.get("region_name"),
            "Country": data.get("country_name"),
            "Latitude": data.get("latitude"),
            "Longitude": data.get("longitude"),
            "Timezone": data.get("time_zone", {}).get("id"),
        }
    else:
        return {"Error": "Unable to fetch geolocation"}

# Function to get weather data
def get_weather(lat, lon, unit="metric"):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units={unit}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "Temperature": data["main"]["temp"],
            "Weather": data["weather"][0]["description"].capitalize(),
            "Humidity": data["main"]["humidity"],
            "Wind Speed": data["wind"]["speed"],
            "Sunrise": datetime.utcfromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M:%S"),
            "Sunset": datetime.utcfromtimestamp(data["sys"]["sunset"]).strftime("%H:%M:%S"),
        }
    else:
        return {"Error": "Unable to fetch weather"}

# Function to get air pollution data
def get_pollution(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        pollution_data = data["list"][0]
        return {
            "AQI": pollution_data["main"]["aqi"],  # Air Quality Index (1=Good, 5=Hazardous)
            "Pollutants": {
                "CO": pollution_data["components"]["co"],  # Carbon Monoxide
                "NO2": pollution_data["components"]["no2"],  # Nitrogen Dioxide
                "O3": pollution_data["components"]["o3"],  # Ozone
                "PM2.5": pollution_data["components"]["pm2_5"],  # Fine Particles
                "PM10": pollution_data["components"]["pm10"],  # Coarse Particles
            }
        }
    else:
        return {"Error": "Unable to fetch pollution data"}

# Function to get 5-day weather forecast
def get_forecast(lat, lon, unit="metric"):
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units={unit}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecast = []
        for item in data["list"]:
            forecast.append({
                "DateTime": item["dt_txt"],
                "Temperature": item["main"]["temp"],
                "Weather": item["weather"][0]["description"].capitalize(),
            })
        return forecast[:5]  # Return next 5 data points (3-hour intervals)
    else:
        return {"Error": "Unable to fetch forecast"}

# Route to serve the frontend
@app.route('/')
def home():
    return render_template('index.html')

# API route to provide data to frontend
@app.route('/api/data')
def api_data():
    visitor_ip = request.remote_addr  # Get visitor's IP
    geolocation = get_geolocation(visitor_ip)
    
    if "Latitude" in geolocation and "Longitude" in geolocation:
        lat, lon = geolocation["Latitude"], geolocation["Longitude"]
        weather = get_weather(lat, lon)
        pollution = get_pollution(lat, lon)
        forecast = get_forecast(lat, lon)
        geolocation["Weather"] = weather
        geolocation["Pollution"] = pollution
        geolocation["Forecast"] = forecast
    
    city = geolocation.get("City", "")
    country = geolocation.get("Country", "")
    geolocation["News"] = get_weather_news(city, country)
    geolocation["Recommendations"] = get_recommendations(weather, pollution)
    # Get local time
    if geolocation.get("Timezone"):
        local_time = datetime.now(pytz.timezone(geolocation["Timezone"]))
        geolocation["LocalTime"] = local_time.strftime("%Y-%m-%d %H:%M:%S")
    else:
        geolocation["LocalTime"] = "N/A"
    return jsonify({
        "data": geolocation,
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)  # Run on public IP, port 80
