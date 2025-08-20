from flask import Flask, render_template, request
import requests
import numpy as np
import pickle

app = Flask(__name__)

# Load model
try:
    model = pickle.load(open('weather_model.pkl', 'rb'))
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

API_KEY = '322fa4ecd4c55970a9a47a763a2fceba'  # Replace with your actual key

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

def get_weather_data(lat, lon):
    """Fetch weather data using coordinates"""
    try:
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            return (
                data['main']['temp'],
                data['main']['humidity'],
                data['wind']['speed'],
                data['main']['pressure']
            )
        print(f"Weather API error: {data.get('message')}")
        return None, None, None, None
    except Exception as e:
        print(f"Weather fetch error: {e}")
        return None, None, None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    weather_data = {}
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
                temp, humidity, wind_speed, pressure = get_weather_data(lat, lon)
                
                if None in (temp, humidity, wind_speed, pressure):
                    error = "Could not fetch weather data"
                else:
                    try:
                        input_features = np.array([[temp, humidity, wind_speed, pressure]])
                        prediction = model.predict(input_features)[0]
                        weather_data = {
                            'City': city,
                            'Country': country,
                            'Temperature': temp,
                            'Humidity': humidity,
                            'Wind Speed': wind_speed,
                            'Pressure': pressure
                        }
                    except Exception as e:
                        error = f"Prediction failed: {str(e)}"

    return render_template('index.html', 
                         prediction=prediction,
                         weather_data=weather_data,
                         error=error)
if __name__ == '__main__':
    app.run(debug=True, port=5001)
