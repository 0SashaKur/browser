import os
import importlib.util
import re
from PyQt5.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QMainWindow, QSizePolicy, QLabel, QTabWidget

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
        self.main_window = main_window  # Stocker la référence à main_window
        # Charger func
        self.const_color()

        # Créer un layout vertical pour l'ensemble de l'interface
        self.main_layout = QVBoxLayout()  # Stocker le layout principal dans un attribut
        self.main_layout.addLayout(self.url_action_bare_layout())  # Ajouter la barre d'URL et les boutons



        # Créer un QTabWidget
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)  # Ajouter le QTabWidget au layout principal

        # Créer un layout horizontal principal pour inclure la barre latérale
        main_h_layout = QHBoxLayout()
        main_h_layout.addLayout(self.sidebar_layout())  # Ajouter la barre latérale
        main_h_layout.addLayout(self.main_layout)              # Ajouter le reste de l'interface

        # Appliquer des styles CSS (QSS)
        self.apply_styles()

        # Ajouter le navigateur à l'interface
        main_window.setCentralWidget(QWidget())
        main_window.centralWidget().setLayout(main_h_layout)

        # Ajouter le navigateur à l'interface
        main_window.browser = main_window.browser
        self.tabs.addTab(main_window.browser, "temp")
        self.new_tab.clicked.connect(lambda: main_window.add_tab("Nouvelle onglet", "google.com"))

        self.go_button.clicked.connect(lambda: main_window.navigate_to_url(self.url_bar.text()))  # Appel de la méthode avec l'URL

    def url_action_bare_layout(self):
        # Créer un layout horizontal pour la barre d'URL et le bouton
        self.back_button = QPushButton("⤛")
        self.forward_button = QPushButton("⤜")
        self.refresh_button = QPushButton("⥁")
        self.back_button.setFixedWidth(60)
        self.forward_button.setFixedWidth(60)

        self.url_bar = QLineEdit()
        self.url_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.url_bar.setPlaceholderText("Entrez l'URL ici")

        self.go_button = QPushButton("Go")
        self.go_button.setFixedWidth(40)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.back_button)
        h_layout.addWidget(self.forward_button)
        h_layout.addWidget(self.refresh_button)
        h_layout.addWidget(self.url_bar)
        h_layout.addWidget(self.go_button)
        return h_layout

    def sidebar_layout(self):
        # Créer une barre latérale

        self.history_button = QPushButton("H")
        self.new_tab = QPushButton("+")
        self.history_button.setFixedWidth(30)  # Réduire la largeur du bouton
        self.new_tab.setFixedWidth(30)  # Réduire la largeur du bouton
        sidebar_layout = QVBoxLayout()
        sidebar_layout.addWidget(self.history_button)
        sidebar_layout.addWidget(self.new_tab)
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

        # Récupérer tous les attributs de l'instance qui sont des widgets
        widgets = [widget for widget in self.__dict__.values() if isinstance(widget, (QLineEdit, QPushButton))]

        self.tabs.setStyleSheet(style)  # Appliquer le style à la barre des onglets
        self.tabs.tabBar().setTabText(self.tabs.tabBar().count() - 1, "X")

        for widget in widgets:
            widget.setStyleSheet(style)  # Appliquer le style à chaque widget