from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt5.QtCore import pyqtSignal

class HistoryWidget(QWidget):
    url_selected = pyqtSignal(str)  # Signal pour l'URL sélectionnée

    def __init__(self, history):
        super().__init__()
        self.setWindowTitle("Historique")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        self.list_widget = QListWidget()

        # Ajouter chaque entrée de l'historique à la liste
        for url, page_name, timestamp in history:
            item = QListWidgetItem(f"{timestamp} - {page_name}")
            item.setData(1, url)  # Stocker l'URL dans l'élément
            self.list_widget.addItem(item)

        layout.addWidget(self.list_widget)
        self.setLayout(layout)

        # Connecter le signal de clic
        self.list_widget.itemClicked.connect(self.on_item_clicked)

    def on_item_clicked(self, item):
        url = item.data(1)  # Récupérer l'URL stockée
        self.url_selected.emit(url)  # Émettre le signal avec l'URL