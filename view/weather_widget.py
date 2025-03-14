import sys
import json
import logging
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QInputDialog, QMenu, QTabWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QTextBrowser
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from pprint import pprint

class WeatherWidget(QWidget):
    
    def __init__(self, tab_name, presenter):
        # Инит
        super().__init__()
        self.tab_name = tab_name
        self.presenter = presenter
        self.initUI()
        self.connectSignals()

    def initUI(self):
        # Виджеты
        
        self.input_city = QLineEdit()
        self.input_city.setPlaceholderText('Введите город')

        self.enter_button = QPushButton('Найти')
        
        self.description_weather = QTextBrowser()

        # Лаяуты
        layout_input_button = QHBoxLayout()
        layout_input_button.addWidget(self.input_city)
        layout_input_button.addWidget(self.enter_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout_input_button)
        main_layout.addWidget(self.description_weather)

        self.setLayout(main_layout)

    def connectSignals(self):
        self.enter_button.clicked.connect(self.search_weather)

    def search_weather(self):
        city = self.input_city.text().split()
        if city == '':
            return
        data = self.presenter.search_weather(city)
        self.display_data(data)

    def display_data(self, data: dict):
        self.description_weather.clear()
        for k, v in data.items():
            self.description_weather.append(f'{k} - {v}')
    
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.enter_button.click()
