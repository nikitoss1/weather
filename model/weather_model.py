import requests
import json
from config.token import API_KEY
from config.link_api_weather import BASE_URL
from pprint import pprint

class WeatherModel:

    def __init__(self):
        self.__BASE_URL = BASE_URL
        self.__appid = API_KEY
        self.__units = 'metric'
        self.__lang = 'ru'


    def __get_weather(self, city):
        params = {
            'q': city,
            'appid': self.__appid,
            'units': self.__units,
            'lang': self.__lang,
        }

        response = requests.get(self.__BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise requests.exceptions.HTTPError(
                f'Ошибка {response.status_code}: {response.reason}'
            )        
    
    def check_weather(self, city):
        try:
            data = self.__get_weather(city)
        except requests.exceptions.HTTPError as e:
            return {"error": str(e)}
        except requests.exceptions.RequestException as e:
            return {"error": f"Ошибка запроса: {e}"}
        
        
        if data:
            city = data['name']
            temperature = data['main']['temp']
            weather_description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']

            return {
                'city': city,
                'temperature': temperature,
                'weather_description': weather_description,
                'humidity': humidity,
                'wind_speed': wind_speed
            }
        else:
            return {'error': 'Данные о погоде не получены'}