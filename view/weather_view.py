import sys
import json
import logging
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QInputDialog, QMenu, QTabWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QTextBrowser
from PyQt6.QtCore import Qt
from view.weather_widget import WeatherWidget

class WeatherView(QMainWindow):

    def __init__(self):
        super().__init__()
        # Парметры окна
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Погода')
        self.setGeometry(2500, 300, 300, 350)
        self.setFixedSize(300, 350)
        
        self.createWidgets()

    def createWidgets(self):
        # Widgets
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        
        self.setCentralWidget(self.tabs)

        self.remove_button = QPushButton('Удалить вкладку')
        
        self.add_button = QPushButton('Добавить вкладку')
        

        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        button_container.setLayout(button_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(button_container)
        main_layout.addWidget(self.tabs)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        
    def connectSignals(self, presenter):
        self.presenter = presenter
        self.tabs.tabCloseRequested.connect(self.remove_tab_by_index)
        self.remove_button.clicked.connect(self.remove_tab)
        self.add_button.clicked.connect(self.add_new_tab)
        self.tabs.tabBar().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tabs.tabBar().customContextMenuRequested.connect(self.show_context_menu)


    def add_new_tab(self):
        tab_name = f'Вкладка {self.tabs.count() + 1}'
        self.add_tab(tab_name)

    def add_tab(self, tab_name):
        tab = WeatherWidget(tab_name, self.presenter)
        self.tabs.addTab(tab, tab_name)

    def remove_tab(self):
        if self.tabs.count() == 1:
            return         
        current_index = self.tabs.currentIndex()
        if current_index != -1:
            self.remove_tab_by_index(current_index)

    def remove_tab_by_index(self, index):
        if self.tabs.count() == 1:
            return 
        if index != -1:
            self.tabs.removeTab(index)

    def show_context_menu(self, position):
        tab_index = self.tabs.tabBar().tabAt(position)
        if tab_index != -1:
            menu = QMenu(self)
            rename_action = menu.addAction('Переименовать')
            rename_action.triggered.connect(lambda: self.rename_tab(tab_index))
            menu.exec(self.tabs.tabBar().mapToGlobal(position))
        
    def rename_tab(self, index):
        if index != -1:
            current_name = self.tabs.tabText(index)
            new_name, ok = QInputDialog.getText(self, 'Переименовать вкладку', 'Новое имя: ', text=current_name)
            if ok and new_name:
                self.tabs.setTabText(index, new_name)
                tab = self.tabs.widget(index)
                tab.tab_name = new_name


if __name__ == '__main__':
    app = QApplication([])
    from presenter.weather_presenter import WeatherPresenter
    o = WeatherPresenter()
    window = WeatherView(o)
    window.show()
    app.exec()






