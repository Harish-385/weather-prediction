# train_model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

# Example dummy data
data = {
    'Temperature': [30, 28, 25, 20, 22, 35, 33, 18, 15, 27],
    'Humidity': [70, 65, 90, 85, 80, 50, 55, 95, 92, 60],
    'Wind Speed': [5, 4, 6, 7, 5.5, 3, 2.5, 8, 7.5, 3.5],
    'Pressure': [1008, 1010, 1005, 1003, 1007, 1012, 1011, 1002, 1001, 1013],
    'Weather': ['Sunny', 'Sunny', 'Rainy', 'Rainy', 'Rainy', 'Sunny', 'Sunny', 'Rainy', 'Rainy', 'Sunny']
}
df = pd.DataFrame(data)
X = df[['Temperature', 'Humidity', 'Wind Speed', 'Pressure']]
y = df['Weather']
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)
# Save the model
with open('weather_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("✅ Model trained and saved as weather_model.pkl")
