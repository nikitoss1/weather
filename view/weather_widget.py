import sys
import json
import logging
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QInputDialog, QMenu, QTabWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QTextBrowser
from PyQt6.QtCore import Qt


class WeatherWidget(QWidget):
    
    def __init__(self, tab_name):
        # Инит
        super().__init__()
        self.tab_name = tab_name
        self.createUI()
        self.create_connections()

    def createUI(self):
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

    def create_connections(self):
        pass
        #self.enter_button.clicked.connect(self.search_weathers)
