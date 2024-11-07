from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from url_manager import URLManager
from ui import Ui_MainWindow  # Importer la classe d'interface utilisateur
import os

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mon Navigateur Firefox")
        self.setGeometry(100, 100, 1200, 800)

        self.url_manager = URLManager()  # Instance du gestionnaire d'URL

        # Créer un profil de navigateur avec un chemin de cache personnalisé
        profile_path = os.path.join(os.getcwd(), 'user_profile')
        self.web_profile = QWebEngineProfile(profile_path, self)
        self.web_profile.setCachePath(profile_path)
        self.web_profile.setPersistentStoragePath(profile_path)

        self.browser = QWebEngineView()
        self.browser.setPage(QWebEnginePage(self.web_profile, self.browser))

        # Initialiser l'interface utilisateur
        self.ui = Ui_MainWindow()
        self.ui.setup_ui(self)

        # Charger Google.com au démarrage
        self.load_homepage()


        self.ui.go_button.clicked.connect(self.navigate_to_url)
        self.ui.back_button.clicked.connect(self.browser.back)
        self.ui.forward_button.clicked.connect(self.browser.forward)
        self.ui.refresh_button.clicked.connect(self.browser.reload)

        # Initialiser l'historique
        self.history = []

    def load_homepage(self):
        self.browser.setUrl(QUrl(self.url_manager.get_homepage()))

    def navigate_to_url(self):
        url = self.ui.url_bar.text()
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
        self.browser.setUrl(QUrl(url))
        self.add_to_history(url)

    def add_to_history(self, url):
        self.history.append(url)

    def show_history(self):
        # Afficher l'historique dans la console pour l'instant
        for url in self.history:
            print(url)
