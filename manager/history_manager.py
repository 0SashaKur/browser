import sqlite3

class HistoryManager:
    def __init__(self, db_path='user_profile/storage_man/history.db'):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                page_name TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.connection.commit()

    def add_to_history(self, url, page_name):
        self.cursor.execute('INSERT INTO history (url, page_name) VALUES (?, ?)', (url, page_name))
        self.connection.commit()

    def get_history(self):
        self.cursor.execute('SELECT url, page_name, timestamp FROM history ORDER BY timestamp DESC')
        return self.cursor.fetchall()  # Renvoie une liste de tuples (url, page_name, timestamp)

    def close(self):
        self.connection.close()
