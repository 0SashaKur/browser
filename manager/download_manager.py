import sqlite3
import os
import requests
from threading import Thread

class DownloadManager:
    def __init__(self, db_path='user_profile/storage_man/download.db', download_path='D:/download'):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_table()
        self.download_path = download_path
        os.makedirs(self.download_path, exist_ok=True)

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS download (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.connection.commit()

    def add_to_download_list(self, file_name):
        self.cursor.execute('INSERT INTO download (file_name) VALUES (?)', (file_name,))
        self.connection.commit()

    def get_download_list(self):
        self.cursor.execute('SELECT * FROM download')
        return self.cursor.fetchall()

    def get_tasks(self):
        tasks = {}
        for row in self.get_download_list():
            tasks[row[1]] = None
        return tasks

    def download_file(self, url):
        local_filename = os.path.join(self.download_path, url.split('/')[-1])
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        self.add_to_download_list(local_filename)

    def start_download(self, url):
        thread = Thread(target=self.download_file, args=(url,))
        thread.start()

    def close(self):
        self.connection.close()
