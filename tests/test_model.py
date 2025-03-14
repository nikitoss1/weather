import unittest
import requests
from unittest.mock import patch, MagicMock
from model.weather_model import WeatherModel

class TestWeatherModel(unittest.TestCase):

    def setUp(self):
        self.weather = WeatherModel()

    @patch('model.weather_model.requests.get')
    def test_check_weather_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "Москва",
            "main": {"temp": 25, "humidity": 60},
            "weather": [{"description": "ясно"}],
            "wind": {"speed": 3.5}
        }

        mock_get.return_value = mock_response

        result = self.weather.check_weather('Москва')
        self.assertIn("city", result)
        self.assertEqual(result["city"], "Москва")
        self.assertEqual(result["temperature"], 25)
        self.assertEqual(result["weather_description"], "ясно")
        self.assertEqual(result["humidity"], 60)
        self.assertEqual(result["wind_speed"], 3.5)

    @patch("model.weather_model.requests.get")
    def test_check_weather_not_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.reason = "Not Found"
        mock_get.return_value = mock_response

        result = self.weather.check_weather("НеизвестныйГород")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Ошибка 404: Not Found")

    @patch("model.weather_model.requests.get")
    def test_check_weather_request_exception(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Ошибка сети")

        result = self.weather.check_weather("Москва")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Ошибка запроса: Ошибка сети")

if __name__ == "__main__":
    unittest.main()
    