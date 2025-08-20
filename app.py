from flask import Flask, render_template, request, jsonify
import requests
import numpy as np
import pickle
import sqlite3
import json
from datetime import datetime, timedelta
import plotly.graph_objs as go
import plotly.utils
import pandas as pd

app = Flask(__name__)

# Load model
try:
    model = pickle.load(open('weather_model.pkl', 'rb'))
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

API_KEY = '322fa4ecd4c55970a9a47a763a2fceba'  # Replace with your actual key

# Initialize database
def init_db():
    conn = sqlite3.connect('weather_history.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            country TEXT,
            date TEXT,
            temperature REAL,
            humidity REAL,
            wind_speed REAL,
            pressure REAL,
            weather_condition TEXT,
            clothing_suggestion TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_coordinates(city, country):
    """Convert city/country to coordinates using OpenWeather Geocoding API"""
    try:
        url = f'http://api.openweathermap.org/geo/1.0/direct?q={city},{country}&limit=1&appid={API_KEY}'
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200 and data:
            return data[0]['lat'], data[0]['lon']
        return None, None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None, None

def get_current_weather(lat, lon):
    """Fetch current weather data using coordinates"""
    try:
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            return {
                'temp': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'pressure': data['main']['pressure'],
                'weather_condition': data['weather'][0]['main'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon']
            }
        print(f"Weather API error: {data.get('message')}")
        return None
    except Exception as e:
        print(f"Weather fetch error: {e}")
        return None

def get_forecast(lat, lon):
    """Fetch 7-day weather forecast"""
    try:
        url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            forecast_data = []
            for item in data['list']:
                forecast_data.append({
                    'date': item['dt_txt'],
                    'temp': item['main']['temp'],
                    'humidity': item['main']['humidity'],
                    'wind_speed': item['wind']['speed'],
                    'weather_condition': item['weather'][0]['main'],
                    'description': item['weather'][0]['description']
                })
            return forecast_data
        return None
    except Exception as e:
        print(f"Forecast fetch error: {e}")
        return None

def get_clothing_suggestion(temp, humidity, weather_condition, wind_speed):
    """AI-based clothing suggestion system"""
    suggestions = []
    
    # Temperature-based suggestions
    if temp >= 30:
        suggestions.extend([
            "👕 Light cotton t-shirt",
            "🩳 Shorts or light pants",
            "🕶️ Sunglasses",
            "🧢 Hat or cap",
            "👟 Light breathable shoes"
        ])
    elif temp >= 20:
        suggestions.extend([
            "👕 Cotton t-shirt or polo",
            "👖 Light pants or jeans",
            "👟 Comfortable shoes",
            "🧥 Light jacket (optional)"
        ])
    elif temp >= 10:
        suggestions.extend([
            "👕 Long-sleeve shirt",
            "👖 Jeans or warm pants",
            "🧥 Light to medium jacket",
            "👟 Closed shoes"
        ])
    elif temp >= 0:
        suggestions.extend([
            "👕 Warm sweater or hoodie",
            "👖 Warm pants",
            "🧥 Medium to heavy jacket",
            "🧤 Gloves",
            "🧣 Scarf",
            "👢 Boots or warm shoes"
        ])
    else:
        suggestions.extend([
            "🧥 Heavy winter coat",
            "👕 Multiple warm layers",
            "👖 Thermal pants",
            "🧤 Heavy gloves",
            "🧣 Warm scarf",
            "👢 Winter boots",
            "🧢 Winter hat"
        ])
    
    # Weather condition-based suggestions
    if 'rain' in weather_condition.lower() or 'drizzle' in weather_condition.lower():
        suggestions.extend([
            "🌂 Umbrella",
            "🧥 Waterproof jacket",
            "👢 Waterproof shoes"
        ])
    elif 'snow' in weather_condition.lower():
        suggestions.extend([
            "🧥 Waterproof winter coat",
            "👢 Waterproof boots",
            "🧤 Waterproof gloves"
        ])
    elif 'storm' in weather_condition.lower() or wind_speed > 10:
        suggestions.extend([
            "🧥 Windproof jacket",
            "🧢 Secure hat",
            "🌂 Strong umbrella (if needed)"
        ])
    
    # Humidity-based suggestions
    if humidity > 80:
        suggestions.append("👕 Moisture-wicking fabrics")
    elif humidity < 30:
        suggestions.append("🧴 Lip balm and moisturizer")
    
    return suggestions

def save_weather_data(city, country, weather_data, clothing_suggestion):
    """Save weather data to database"""
    try:
        conn = sqlite3.connect('weather_history.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO weather_history 
            (city, country, date, temperature, humidity, wind_speed, pressure, weather_condition, clothing_suggestion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            city, country, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            weather_data['temp'], weather_data['humidity'], weather_data['wind_speed'],
            weather_data['pressure'], weather_data['weather_condition'],
            json.dumps(clothing_suggestion)
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")

def get_weather_history(city, country, days=7):
    """Get weather history for the specified city"""
    try:
        conn = sqlite3.connect('weather_history.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT date, temperature, humidity, wind_speed, pressure, weather_condition
            FROM weather_history 
            WHERE city = ? AND country = ?
            ORDER BY date DESC
            LIMIT ?
        ''', (city, country, days))
        data = cursor.fetchall()
        conn.close()
        
        if data:
            return [{
                'date': row[0],
                'temperature': row[1],
                'humidity': row[2],
                'wind_speed': row[3],
                'pressure': row[4],
                'weather_condition': row[5]
            } for row in data]
        return []
    except Exception as e:
        print(f"History fetch error: {e}")
        return []

def create_weather_charts(forecast_data, history_data):
    """Create weather trend charts using Plotly"""
    charts = {}
    
    if forecast_data:
        # Temperature chart
        dates = [item['date'] for item in forecast_data]
        temps = [item['temp'] for item in forecast_data]
        
        temp_fig = go.Figure()
        temp_fig.add_trace(go.Scatter(
            x=dates, y=temps,
            mode='lines+markers',
            name='Temperature (°C)',
            line=dict(color='#ff6b6b', width=3),
            marker=dict(size=8)
        ))
        temp_fig.update_layout(
            title='7-Day Temperature Forecast',
            xaxis_title='Date',
            yaxis_title='Temperature (°C)',
            template='plotly_white',
            height=400
        )
        charts['temperature'] = json.dumps(temp_fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Humidity chart
        humidity = [item['humidity'] for item in forecast_data]
        hum_fig = go.Figure()
        hum_fig.add_trace(go.Scatter(
            x=dates, y=humidity,
            mode='lines+markers',
            name='Humidity (%)',
            line=dict(color='#4ecdc4', width=3),
            marker=dict(size=8)
        ))
        hum_fig.update_layout(
            title='7-Day Humidity Forecast',
            xaxis_title='Date',
            yaxis_title='Humidity (%)',
            template='plotly_white',
            height=400
        )
        charts['humidity'] = json.dumps(hum_fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    if history_data:
        # Historical comparison chart
        hist_dates = [item['date'] for item in history_data]
        hist_temps = [item['temperature'] for item in history_data]
        
        hist_fig = go.Figure()
        hist_fig.add_trace(go.Scatter(
            x=hist_dates, y=hist_temps,
            mode='lines+markers',
            name='Historical Temperature',
            line=dict(color='#95a5a6', width=2, dash='dash'),
            marker=dict(size=6)
        ))
        hist_fig.update_layout(
            title='Historical Temperature Comparison',
            xaxis_title='Date',
            yaxis_title='Temperature (°C)',
            template='plotly_white',
            height=400
        )
        charts['history'] = json.dumps(hist_fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return charts

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    weather_data = {}
    clothing_suggestions = []
    forecast_data = []
    history_data = []
    charts = {}
    prediction = None

    if request.method == 'POST':
        city = request.form.get('city', '').strip()
        country = request.form.get('country', '').strip()

        if not city or not country:
            error = "Please enter both city and country"
        else:
            lat, lon = get_coordinates(city, country)
            
            if lat is None or lon is None:
                error = f"Could not find coordinates for {city}, {country}"
            else:
                # Get current weather
                current_weather = get_current_weather(lat, lon)
                
                if current_weather is None:
                    error = "Could not fetch weather data"
                else:
                    # Get clothing suggestions
                    clothing_suggestions = get_clothing_suggestion(
                        current_weather['temp'],
                        current_weather['humidity'],
                        current_weather['weather_condition'],
                        current_weather['wind_speed']
                    )
                    
                    # Get forecast
                    forecast_data = get_forecast(lat, lon)
                    
                    # Get history
                    history_data = get_weather_history(city, country)
                    
                    # Create charts
                    charts = create_weather_charts(forecast_data, history_data)
                    
                    # Save to database
                    save_weather_data(city, country, current_weather, clothing_suggestions)
                    
                    # Make prediction if model is available
                    if model:
                        try:
                            input_features = np.array([[
                                current_weather['temp'],
                                current_weather['humidity'],
                                current_weather['wind_speed'],
                                current_weather['pressure']
                            ]])
                            prediction = model.predict(input_features)[0]
                        except Exception as e:
                            print(f"Prediction error: {e}")
                    
                    weather_data = {
                        'City': city,
                        'Country': country,
                        'Temperature': current_weather['temp'],
                        'Humidity': current_weather['humidity'],
                        'Wind Speed': current_weather['wind_speed'],
                        'Pressure': current_weather['pressure'],
                        'Condition': current_weather['weather_condition'],
                        'Description': current_weather['description'],
                        'Icon': current_weather['icon']
                    }

    return render_template('index.html', 
                         prediction=prediction,
                         weather_data=weather_data,
                         clothing_suggestions=clothing_suggestions,
                         forecast_data=forecast_data,
                         history_data=history_data,
                         charts=charts,
                         error=error)

@app.route('/api/weather/<city>/<country>')
def api_weather(city, country):
    """API endpoint for weather data"""
    lat, lon = get_coordinates(city, country)
    if lat and lon:
        weather = get_current_weather(lat, lon)
        if weather:
            clothing = get_clothing_suggestion(
                weather['temp'],
                weather['humidity'],
                weather['weather_condition'],
                weather['wind_speed']
            )
            return jsonify({
                'weather': weather,
                'clothing_suggestions': clothing
            })
    return jsonify({'error': 'Could not fetch weather data'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5001)
