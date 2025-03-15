import requests
import json
from googletrans import Translator
from config.token import API_KEY
from config.link_api_weather import BASE_URL
from pprint import pprint

class WeatherModel:

    def __init__(self):
        self.__BASE_URL = BASE_URL
        self.__appid = API_KEY
        self.__units = 'metric'
        self.__lang = 'ru'
        self.translator = Translator()

        with open('city_list/city.list.json', encoding='utf-8') as file:
            self.cities = json.load(file)

    def find_city(self, city_name):
        city_name = " ".join(city_name)
        for city in self.cities:
            if city['name'].lower() == city_name.lower():
                return city['id']

    def __get_weather(self, city):
        id = self.find_city(city)
        params = {
            'id': id,
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
        city[0] = self.translator.translate(city[0], dest='en').text
        try:
            data = self.__get_weather(city)
        except requests.exceptions.HTTPError as e:
            return {"error": str(e)}
        except requests.exceptions.RequestException as e:
            return {"error": f"Ошибка запроса: {e}"}
        
        if data:
            city = data['name']
            country = data['sys']['country']
            temperature = data['main']['temp']
            weather_description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']

            return {
                'city': city,
                'country': country,
                'temperature': temperature,
                'weather_description': weather_description,
                'humidity': humidity,
                'wind_speed': wind_speed
            }
        else:
            return {'error': 'Данные о погоде не получены'}