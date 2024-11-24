# Weather Dashboard

## **Overview**
The **Weather Dashboard** provides users with real-time information about their location, weather conditions, air quality index (AQI), and weather-related news without requiring access to their device's location services. It combines geolocation, weather, pollution, and news data to create a visually engaging and actionable dashboard.

### **Key Features**
- **Real-Time Weather Data**: Displays temperature, humidity, weather conditions, sunrise/sunset times, and wind speed.
- **Air Quality Index (AQI)**: Visual representation of AQI with detailed pollutant information.
- **Weather-Related News**: Shows relevant news articles based on the user's geolocation and weather.
- **Recommendations**: Offers actionable advice based on weather and air quality (e.g., "Bring an umbrella" or "Wear a mask").
- **Weather Forecast**: Displays a 5-day forecast with temperature and weather conditions.

---

## **File Structure**
The project is structured as follows:

```
project/
├── app.py                   # Main Flask application backend
├── templates/
│   └── index.html           # Main HTML file for the dashboard
├── static/
│   ├── css/
│   │   └── styles.css       # Styling for the dashboard
│   └── js/
│       └── script.js        # Frontend logic (fetching API data and populating the UI)
├── requirements.txt         # Python dependencies for the project
└── README.md                # Documentation for the project
```


### **File Descriptions**
1. **`app.py`**:
   - Backend logic using Flask.
   - Fetches user geolocation, weather, air quality, and news data from APIs.
   - Includes endpoints like `/api/data` to serve JSON data to the frontend.
   - Generates recommendations based on weather and AQI data.

2. **`templates/index.html`**:
   - HTML structure of the dashboard.
   - Displays geolocation, weather, pollution, forecast, news, and recommendations in an organized layout.

3. **`static/css/styles.css`**:
   - Contains all the styles for the dashboard.
   - Includes responsive designs, color schemes, and hover effects.

4. **`static/js/script.js`**:
   - Handles fetching data from the backend (`/api/data`).
   - Dynamically updates the dashboard with fetched data (e.g., weather, news, AQI chart).

5. **`requirements.txt`**:
   - Lists all Python dependencies required for the project.
   - Includes Flask, requests, and any other necessary libraries.

6. **`README.md`**:
   - Documentation file (this file).
   - Explains the purpose, features, file structure, and setup instructions.

---

## **APIs Used**
This project integrates the following APIs:
1. **ipstack API**:
   - Provides geolocation data based on the user's public IP address.
2. **OpenWeather API**:
   - Fetches current weather, pollution data, and 5-day forecasts.
3. **NewsAPI**:
   - Fetches weather-related news articles based on the user's location and weather conditions.

---

## **Setup Instructions**
Follow these steps to set up and run the dashboard locally:

### **1. Clone the Repository**
```
git clone https://github.com/heheJY/weather-dashboard.git 
cd weather-dashboard
```

### **2. Create a Virtual Environment**

```
python -m venv venv
source venv/bin/activate   
venv\Scripts\activate      
```

### **3. Install Dependencies**
```
pip install -r requirements.txt
```

### **4. Set API Keys**
```
Update the following placeholders in app.py with your API keys:

IPSTACK_API_KEY for ipstack API.
OPENWEATHER_API_KEY for OpenWeather API.
NEWS_API_KEY for NewsAPI.
```

### **5. Start the Flask server**
```
flask run
```

## **How to Use the Dashboard**
1. Open the dashboard in your browser: [http://127.0.0.1:5000/](http://127.0.0.1:5000/).
2. The following information is displayed:
   - **Location**: City, region, and country based on your public IP.
   - **Weather**: Real-time weather details such as temperature, humidity, and conditions.
   - **Pollution**: AQI with detailed pollutants and a dynamic AQI chart.
   - **News**: Weather-related articles from reliable sources.
   - **Recommendations**: Personalized advice based on weather and pollution.
   - **Forecast**: A 5-day weather forecast.

---

## **Customization**

You can customize the dashboard by:
- Adding more conditions for recommendations in `get_recommendations` (e.g., for wind speeds).
- Adjusting the layout in `styles.css` for unique designs.
- Modifying the API calls in `app.py` for additional data (e.g., hourly forecasts).

---

## **Screenshots**
![Dashboard](/images/Screenshot%201.png)
![AQI Chart and Forecast](/images/Screenshot%202.png)

