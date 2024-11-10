from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton
from PyQt5.QtCore import dec, pyqtSignal

class DownloadWidget(QWidget):
    download_finished = pyqtSignal(str)  # Signal pour indiquer la fin du téléchargement

    def __init__(self, download):
        super().__init__()
        self.setWindowTitle("Téléchargement")
        self.setGeometry(100, 100, 400, 300)

        self.set_download(download)

    def set_download(self, download):
        layout = QVBoxLayout()
        self.list_widget = QListWidget()

        for doc in download:
            item = QListWidgetItem(f"{doc[1]} - {doc[2]}") # Stockage du nom du document dans l'élément
            self.list_widget.addItem(item)

        layout.addWidget(self.list_widget)
        self.setLayout(layout)


    def on_item_clicked(self, item):
        task_name = item.data(1)
        self.download_finished.emit(task_name)  # Emettre le signal de fin de téléchargement