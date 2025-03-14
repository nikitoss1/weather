class WeatherPresenter:

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.connectSignals(self)
        self.view.add_new_tab()

    def search_weather(self, city):
        data = self.model.check_weather(city)
        return data