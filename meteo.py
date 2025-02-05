import requests
import json
import ftfy  # Import du module ftfy
from datetime import datetime, timedelta
import os

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")

def get_weather_data(city):
    key = api_key  # Ta clé d'API OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=fr"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()  # Désérialiser la réponse JSON
        
        # Extraire les données nécessaires pour la météo actuelle
        current_weather = data['list'][0]
        current_temp = current_weather['main']['temp']
        condition = current_weather['weather'][0]['description']
        condition = ftfy.fix_text(condition)

        # Récupérer la date actuelle et les jours suivants
        today = datetime.today()
        tomorrow = today + timedelta(days=1)
        day_after_tomorrow = today + timedelta(days=2)

        forecast = []
        # Récupération des prévisions pour demain et après-demain
        for i in range(8, 24, 8):  # Prévisions tous les 8h pour les 2 jours suivants
            day_forecast = data['list'][i]
            day_max = day_forecast['main']['temp_max']
            day_min = day_forecast['main']['temp_min']
            day_condition = day_forecast['weather'][0]['description']
            day_condition = ftfy.fix_text(day_condition)

            # Associer la prévision à un jour spécifique
            forecast_date = tomorrow if i == 8 else day_after_tomorrow
            forecast_day = forecast_date.strftime("%A")  # Obtenir le jour de la semaine (ex: "Thursday")
            
            forecast.append({
                'forecast_day': forecast_day,
                'temp_max': day_max,
                'temp_min': day_min,
                'condition': day_condition
            })

        # Retourner les données
        result = {
            'currentTemp': current_temp,
            'currentCondition': condition,
            'forecast': forecast
        }
        
        return json.dumps(result, ensure_ascii=False)
    else:
        return json.dumps({'error': 'Failed to retrieve data'})
