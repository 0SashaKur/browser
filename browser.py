from datetime import datetime
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow, QPushButton, QListWidgetItem
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from manager.url_manager import URLManager
from ui import Ui_MainWindow, load_ui_files
from ui_dos.history import HistoryWidget
from manager.history_manager import HistoryManager
import os

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mon Navigateur Firefox")
        self.setGeometry(100, 100, 1200, 800)

        self.url_manager = URLManager()
        self.history_manager = HistoryManager()

        profile_path = os.path.join(os.getcwd(), 'user_profile')
        self.web_profile = QWebEngineProfile(profile_path, self)
        self.web_profile.setCachePath(profile_path)
        self.web_profile.setPersistentStoragePath(profile_path)

        self.browser = QWebEngineView()
        self.browser.setPage(QWebEnginePage(self.web_profile, self.browser))

        self.ui = Ui_MainWindow()
        self.ui.setup_ui(self)

        self.load_homepage()

        self.browser.loadFinished.connect(self.on_page_load)
        self.ui.go_button.clicked.connect(self.navigate_to_url)
        self.ui.back_button.clicked.connect(self.browser.back)
        self.ui.forward_button.clicked.connect(self.browser.forward)
        self.ui.refresh_button.clicked.connect(self.browser.reload)
        self.ui.history_button.clicked.connect(self.toggle_history)

        load_ui_files('ui_dos')

        self.history_widget = HistoryWidget(self.history_manager.get_history())
        self.history_widget.setVisible(False)
        self.ui.main_layout.addWidget(self.history_widget)

        # Connecter le signal url_selected à la méthode load_url_from_history
        self.history_widget.url_selected.connect(self.load_url_from_history)

    def load_homepage(self):
        self.browser.setUrl(QUrl(self.url_manager.get_homepage()))

    def navigate_to_url(self):
        url = self.ui.url_bar.text()
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
        self.browser.setUrl(QUrl(url))

    def load_url_from_history(self, url):
        self.browser.setUrl(QUrl(url))  # Charger l'URL sélectionnée

    def add_to_history(self, url, page_name):
        if url not in [entry[0] for entry in self.history_manager.get_history()]:
            self.history_manager.add_to_history(url, page_name)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.history_widget.list_widget.insertItem(0, f"{timestamp} - {page_name} - {url}")

    def toggle_history(self):
        self.history_widget.setVisible(not self.history_widget.isVisible())

    def on_page_load(self):
        current_url = self.browser.url().toString()
        page_name = self.browser.title()
        self.add_to_history(current_url, page_name)

    def closeEvent(self, event):
        self.history_manager.close()
        super().closeEvent(event)