from datetime import datetime
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow, QPushButton, QListWidgetItem, QWidget, QVBoxLayout
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

        # Assurez-vous que self.ui.tabs est bien initialisé dans setup_ui
        self.tabs = self.ui.tabs

        self.load_homepage()

        self.browser.loadFinished.connect(self.on_page_load)
        # self.ui.go_button.clicked.connect(self.navigate_to_url)
        self.ui.back_button.clicked.connect(self.navigate_back)
        self.ui.forward_button.clicked.connect(self.navigate_forward)
        self.ui.refresh_button.clicked.connect(self.refresh_current_tab)
        self.ui.history_button.clicked.connect(self.toggle_history)

        load_ui_files('ui_dos')

        self.history_widget = HistoryWidget(self.history_manager.get_history())
        self.history_widget.setVisible(False)
        self.ui.main_layout.addWidget(self.history_widget)

        # Connecter le signal url_selected à la méthode load_url_from_history
        self.history_widget.url_selected.connect(self.load_url_from_history)

        self.ui.tabs.currentChanged.connect(self.update_url_placeholder)  # Connecter le changement d'onglet

        self.ui.tabs.tabBar().setTabsClosable(True)  # Permettre la fermeture des onglets
        self.ui.tabs.tabBar().tabCloseRequested.connect(self.close_tab)  # Connecter le signal de fermeture

    def add_tab(self, title, url):
        tab = QWebEngineView()
        tab.setPage(QWebEnginePage(self.web_profile, tab))
        tab.loadFinished.connect(self.on_page_load)  # Connecter le signal pour chaque nouvel onglet
        self.navigate_to_url(url, tab)
        self.ui.tabs.addTab(tab, title)

    def load_homepage(self):
        self.browser.setUrl(QUrl(self.url_manager.get_homepage()))

    def navigate_to_url(self, url, tab=None):
        if tab is None:
            tab = self.tabs.currentWidget()
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
        tab.setUrl(QUrl(url))

    def load_url_from_history(self, url):
        current_tab = self.tabs.currentWidget()
        current_tab.setUrl(QUrl(url))  # Charger l'URL sélectionnée dans l'onglet actuel

    def add_to_history(self, url, page_name):
        if url not in [entry[0] for entry in self.history_manager.get_history()]:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.history_manager.add_to_history(url, page_name)
            item = QListWidgetItem(f"{timestamp} - {page_name}")
            item.setData(1, url)  # Stocker l'URL dans l'élément
            self.history_widget.list_widget.insertItem(0, item)

    def toggle_history(self):
        self.history_widget.setVisible(not self.history_widget.isVisible())

    def on_page_load(self, success):
        if success:  # Vérifiez si le chargement a réussi
            current_tab = self.tabs.currentWidget()
            current_url = current_tab.url().toString()
            page_name = current_tab.title()
            self.add_to_history(current_url, page_name)
            index = self.ui.tabs.indexOf(current_tab)  # Obtenir l'index de l'onglet
            self.set_tab_name(current_tab, page_name)  # Changer le nom de l'onglet
            self.ui.url_bar.setText(current_url)  # Mettre à jour le placeholder avec l'URL actuelle

    def set_tab_name(self, tab, name):
        index = self.ui.tabs.indexOf(tab)  # Obtenir l'index de l'onglet
        self.ui.tabs.setTabText(index, name)  # Changer le nom de l'onglet

    def closeEvent(self, event):
        self.history_manager.close()
        super().closeEvent(event)

    def update_url_placeholder(self, index):
        current_tab = self.tabs.widget(index)  # Obtenir l'onglet actuel
        if current_tab:
            current_url = current_tab.url().toString()  # Obtenir l'URL de l'onglet
            self.ui.url_bar.setText(current_url)  # Mettre à jour le placeholder avec l'URL actuelle

    def navigate_back(self):
        current_tab = self.tabs.currentWidget()  # Obtenir l'onglet actuel
        if current_tab:
            current_tab.back()  # Appeler la méthode back sur l'onglet actuel

    def navigate_forward(self):
        current_tab = self.tabs.currentWidget()  # Obtenir l'onglet actuel
        if current_tab:
            current_tab.forward()  # Appeler la méthode forward sur l'onglet actuel

    def refresh_current_tab(self):
        current_tab = self.tabs.currentWidget()  # Obtenir l'onglet actuel
        if current_tab:
            current_tab.reload()  # Appeler la méthode reload sur l'onglet actuel

    def close_tab(self, index):
        if index >= 0:  # Vérifier que l'index est valide
            self.ui.tabs.removeTab(index)  # Fermer l'onglet à l'index donné