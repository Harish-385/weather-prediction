# 🌤️ AI Weather & Clothing Assistant

A smart weather application that provides AI-based clothing suggestions and weather history tracking with interactive charts.

## ✨ Features

### 👕 AI-Based Clothing Suggestions
- **Temperature-based recommendations**: Light clothes for hot weather, warm layers for cold
- **Weather condition awareness**: Umbrella for rain, waterproof gear for snow
- **Humidity considerations**: Moisture-wicking fabrics for high humidity
- **Wind protection**: Windproof jackets for stormy conditions

### 📊 Weather History & Trends
- **7-day forecast**: Detailed temperature and humidity predictions
- **Interactive charts**: Beautiful Plotly charts for temperature and humidity trends
- **Historical comparison**: Compare current weather with past data
- **Data persistence**: SQLite database stores weather history

### 🌍 Smart Location Search
- **Global coverage**: Search any city worldwide
- **Real-time data**: Live weather data from OpenWeatherMap API
- **Accurate coordinates**: Automatic geocoding for precise weather data

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd weather-prediction
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get API Key**
   - Sign up at [OpenWeatherMap](https://openweathermap.org/api)
   - Get your free API key
   - Replace the API key in `app.py` (line 15)

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   - Navigate to `http://localhost:5001`

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Plotly.js
- **Database**: SQLite
- **Weather API**: OpenWeatherMap
- **Icons**: Font Awesome
- **Styling**: Custom CSS with modern gradients

## 📱 Features in Detail

### Clothing Suggestions System
The AI analyzes multiple weather factors to provide personalized clothing recommendations:

- **Temperature ranges**:
  - 30°C+: Light cotton clothes, sunglasses, hat
  - 20-29°C: Cotton t-shirt, light pants, comfortable shoes
  - 10-19°C: Long-sleeve shirt, jeans, light jacket
  - 0-9°C: Warm sweater, jacket, gloves, scarf
  - Below 0°C: Heavy winter coat, thermal layers, winter boots

- **Weather conditions**:
  - Rain: Umbrella, waterproof jacket and shoes
  - Snow: Waterproof winter gear
  - Storm/Wind: Windproof jacket, secure hat

- **Humidity factors**:
  - High humidity (>80%): Moisture-wicking fabrics
  - Low humidity (<30%): Lip balm and moisturizer

### Weather History & Analytics
- **7-day forecast charts**: Interactive temperature and humidity trends
- **Historical data**: Compare with previous weather patterns
- **Data visualization**: Beautiful, responsive charts
- **Local storage**: SQLite database for data persistence

## 🎨 UI/UX Features

- **Modern design**: Gradient backgrounds and smooth animations
- **Responsive layout**: Works on desktop, tablet, and mobile
- **Interactive elements**: Hover effects and smooth transitions
- **Loading states**: Visual feedback during data fetching
- **Error handling**: User-friendly error messages

## 🔧 API Endpoints

- `GET /`: Main application interface
- `POST /`: Submit location for weather data
- `GET /api/weather/<city>/<country>`: JSON API for weather data

## 📊 Database Schema

```sql
CREATE TABLE weather_history (
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
);
```

## 🚀 Future Enhancements

- [ ] User accounts and personalized history
- [ ] Push notifications for weather alerts
- [ ] Integration with calendar for event planning
- [ ] Seasonal clothing recommendations
- [ ] UV index and sun protection advice
- [ ] Air quality integration
- [ ] Multi-language support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenWeatherMap for weather data API
- Font Awesome for icons
- Plotly for interactive charts
- Flask community for the web framework

---

**Made with ❤️ for better weather planning and smart clothing choices!**
