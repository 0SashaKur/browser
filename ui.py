import os
import importlib.util
import re
from PyQt5.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QMainWindow, QSizePolicy

def load_ui_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.py'):
            filepath = os.path.join(directory, filename)
            module_name = filename[:-3]  # Retirer l'extension .py
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

class Ui_MainWindow:
    def setup_ui(self, main_window):
        # Charger func
        self.const_color()

        # Créer un layout vertical pour l'ensemble de l'interface
        self.main_layout = QVBoxLayout()  # Stocker le layout principal dans un attribut
        self.main_layout.addLayout(self.create_h_layout())

        # Créer un layout horizontal principal pour inclure la barre latérale
        main_h_layout = QHBoxLayout()
        main_h_layout.addLayout(self.create_sidebar_layout())  # Ajouter la barre latérale
        main_h_layout.addLayout(self.main_layout)              # Ajouter le reste de l'interface

        # Appliquer des styles CSS (QSS)
        self.apply_styles()

        # Ajouter le navigateur à l'interface
        main_window.setCentralWidget(QWidget())
        main_window.centralWidget().setLayout(main_h_layout)

        # Ajouter le navigateur à l'interface
        main_window.browser = main_window.browser  # Référence au navigateur
        self.main_layout.addWidget(main_window.browser)

    def create_h_layout(self):
        # Créer un layout horizontal pour la barre d'URL et le bouton
        self.back_button = QPushButton("⤛")
        self.forward_button = QPushButton("⤜")
        self.refresh_button = QPushButton("⥁")
        self.back_button.setFixedWidth(60)
        self.forward_button.setFixedWidth(60)

        self.url_bar = QLineEdit()
        self.url_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.go_button = QPushButton("Go")
        self.go_button.setFixedWidth(40)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.back_button)
        h_layout.addWidget(self.forward_button)
        h_layout.addWidget(self.refresh_button)
        h_layout.addWidget(self.url_bar)
        h_layout.addWidget(self.go_button)
        return h_layout

    def create_sidebar_layout(self):
        # Créer une barre latérale

        self.history_button = QPushButton("H")
        self.sidebar_button2 = QPushButton("")
        self.history_button.setFixedWidth(30)  # Réduire la largeur du bouton
        self.sidebar_button2.setFixedWidth(30)  # Réduire la largeur du bouton
        sidebar_layout = QVBoxLayout()
        sidebar_layout.addWidget(self.history_button)
        sidebar_layout.addWidget(self.sidebar_button2)
        sidebar_layout.addStretch()
        return sidebar_layout

    def const_color(self):
        self.css_color = {
            "--primary": "#7028E3",
            "--primary_hover": "#5826aa",
            "--secondary": "#9452DC",
            "--tertiary": "#AA6DD7",
            "--support": "#C78FD1",
            "--light_accent": "#E5B2CA",
            "--font_color": "#4A1C59"
        }

    def apply_styles(self):
        with open("css/ui.css", "r") as file:
            style = file.read()
        for key, value in self.css_color.items():
            style = re.sub(rf"{key}(\s|;)", f"{value}\\1", style)
        # Appliquer le style à l'application
        self.url_bar.setStyleSheet(style)
        self.go_button.setStyleSheet(style)
        self.back_button.setStyleSheet(style)
        self.forward_button.setStyleSheet(style)
        self.refresh_button.setStyleSheet(style)
        self.history_button.setStyleSheet(style)