from PyQt6.QtWidgets import QApplication
from model.weather_model import WeatherModel
from view.weather_view import WeatherView
from presenter.weather_presenter import WeatherPresenter

if __name__ == '__main__':
    app = QApplication([])

    model = WeatherModel()
    view = WeatherView()
    presenter = WeatherPresenter(model, view)

    view.show()
    app.exec()