#!/usr/bin/env python3
"""
Demo script for AI Weather & Clothing Assistant
Shows the key features without needing the Flask app running
"""

import json
from datetime import datetime

def demo_clothing_suggestions():
    """Demonstrate the AI clothing suggestion system"""
    print("👕 AI-Based Clothing Suggestions Demo")
    print("=" * 50)
    
    # Sample weather scenarios
    scenarios = [
        {
            "name": "Hot Summer Day",
            "temp": 32,
            "humidity": 70,
            "condition": "Clear",
            "wind": 5,
            "location": "Miami, US"
        },
        {
            "name": "Rainy Autumn Day", 
            "temp": 15,
            "humidity": 85,
            "condition": "Rain",
            "wind": 8,
            "location": "London, GB"
        },
        {
            "name": "Cold Winter Day",
            "temp": -5,
            "humidity": 60,
            "condition": "Snow",
            "wind": 12,
            "location": "Moscow, RU"
        },
        {
            "name": "Pleasant Spring Day",
            "temp": 25,
            "humidity": 30,
            "condition": "Clear",
            "wind": 3,
            "location": "Tokyo, JP"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🌤️ {scenario['name']} - {scenario['location']}")
        print(f"   Temperature: {scenario['temp']}°C")
        print(f"   Humidity: {scenario['humidity']}%")
        print(f"   Weather: {scenario['condition']}")
        print(f"   Wind: {scenario['wind']} m/s")
        
        suggestions = get_clothing_suggestions(scenario)
        print("   👕 AI Clothing Suggestions:")
        for suggestion in suggestions:
            print(f"      • {suggestion}")

def get_clothing_suggestions(weather):
    """AI-based clothing suggestion logic"""
    suggestions = []
    temp = weather['temp']
    humidity = weather['humidity']
    condition = weather['condition']
    wind = weather['wind']
    
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
    if 'rain' in condition.lower():
        suggestions.extend([
            "🌂 Umbrella",
            "🧥 Waterproof jacket",
            "👢 Waterproof shoes"
        ])
    elif 'snow' in condition.lower():
        suggestions.extend([
            "🧥 Waterproof winter coat",
            "👢 Waterproof boots",
            "🧤 Waterproof gloves"
        ])
    elif wind > 10:
        suggestions.extend([
            "🧥 Windproof jacket",
            "🧢 Secure hat"
        ])
    
    # Humidity-based suggestions
    if humidity > 80:
        suggestions.append("👕 Moisture-wicking fabrics")
    elif humidity < 30:
        suggestions.append("🧴 Lip balm and moisturizer")
    
    return suggestions

def demo_weather_history():
    """Demonstrate weather history and trends"""
    print("\n📊 Weather History & Trends Demo")
    print("=" * 50)
    
    # Sample historical data
    history_data = {
        "location": "New York, US",
        "current_week": [
            {"date": "2024-01-01", "temp": 22, "humidity": 65, "condition": "Clear"},
            {"date": "2024-01-02", "temp": 24, "humidity": 70, "condition": "Partly Cloudy"},
            {"date": "2024-01-03", "temp": 26, "humidity": 68, "condition": "Clear"},
            {"date": "2024-01-04", "temp": 23, "humidity": 72, "condition": "Rain"},
            {"date": "2024-01-05", "temp": 25, "humidity": 69, "condition": "Clear"},
            {"date": "2024-01-06", "temp": 27, "humidity": 71, "condition": "Partly Cloudy"},
            {"date": "2024-01-07", "temp": 28, "humidity": 67, "condition": "Clear"}
        ],
        "last_year_same_day": [
            {"date": "2023-01-01", "temp": 20, "humidity": 70, "condition": "Cloudy"},
            {"date": "2023-01-02", "temp": 18, "humidity": 75, "condition": "Rain"},
            {"date": "2023-01-03", "temp": 22, "humidity": 68, "condition": "Clear"},
            {"date": "2023-01-04", "temp": 19, "humidity": 80, "condition": "Snow"},
            {"date": "2023-01-05", "temp": 21, "humidity": 72, "condition": "Partly Cloudy"},
            {"date": "2023-01-06", "temp": 23, "humidity": 69, "condition": "Clear"},
            {"date": "2023-01-07", "temp": 25, "humidity": 65, "condition": "Clear"}
        ]
    }
    
    print(f"📍 Location: {history_data['location']}")
    print(f"📅 Current Week vs Last Year Comparison")
    
    print("\n📈 Current Week Forecast:")
    for day in history_data['current_week']:
        print(f"   {day['date']}: {day['temp']}°C, {day['humidity']}% humidity, {day['condition']}")
    
    print("\n📉 Last Year Same Period:")
    for day in history_data['last_year_same_day']:
        print(f"   {day['date']}: {day['temp']}°C, {day['humidity']}% humidity, {day['condition']}")
    
    # Calculate trends
    current_avg = sum(day['temp'] for day in history_data['current_week']) / 7
    last_year_avg = sum(day['temp'] for day in history_data['last_year_same_day']) / 7
    
    print(f"\n📊 Trend Analysis:")
    print(f"   Current week average: {current_avg:.1f}°C")
    print(f"   Last year average: {last_year_avg:.1f}°C")
    print(f"   Temperature difference: {current_avg - last_year_avg:+.1f}°C")
    
    if current_avg > last_year_avg:
        print("   📈 Warmer than last year")
    else:
        print("   📉 Cooler than last year")

def demo_features():
    """Show all the key features"""
    print("🚀 AI Weather & Clothing Assistant - Feature Demo")
    print("=" * 60)
    
    print("\n✨ Key Features:")
    print("   👕 AI-Based Clothing Suggestions")
    print("   📊 Weather History & Trends")
    print("   🌍 Global Location Search")
    print("   📈 Interactive Charts")
    print("   💾 Data Persistence")
    print("   📱 Responsive Design")
    
    print("\n🎯 Smart Clothing Logic:")
    print("   • Temperature-based recommendations")
    print("   • Weather condition awareness")
    print("   • Humidity considerations")
    print("   • Wind protection advice")
    
    print("\n📊 Weather Analytics:")
    print("   • 7-day forecast with charts")
    print("   • Historical data comparison")
    print("   • Temperature and humidity trends")
    print("   • Interactive Plotly visualizations")
    
    print("\n🌐 Technical Features:")
    print("   • Flask web framework")
    print("   • SQLite database")
    print("   • OpenWeatherMap API integration")
    print("   • Modern responsive UI")
    print("   • Real-time data updates")

def main():
    """Run the complete demo"""
    demo_features()
    demo_clothing_suggestions()
    demo_weather_history()
    
    print("\n" + "=" * 60)
    print("🎉 Demo completed successfully!")
    print("\n💡 To use the full application:")
    print("   1. Install dependencies: pip install -r requirements.txt")
    print("   2. Get OpenWeatherMap API key")
    print("   3. Run: python app.py")
    print("   4. Visit: http://localhost:5001")
    print("\n🌟 Enjoy your AI-powered weather and clothing assistant!")

if __name__ == "__main__":
    main()
