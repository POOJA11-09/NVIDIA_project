import sqlite3
import hashlib
 
 
def make_hash(text: str):
    return hashlib.md5(text.encode("utf-8")).hexdigest()
 
 
class DB:
 
    def __init__(self):
        self.conn = sqlite3.connect("intel.db")
        self.create_table()
 
    def create_table(self):
        cursor = self.conn.cursor()
 
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            content_hash TEXT UNIQUE,
            source TEXT,
            category TEXT,
            url TEXT UNIQUE,
            published_date TEXT,
            collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
 
        self.conn.commit()
 
    def insert(self, title, content, source, category, url, date):
        cursor = self.conn.cursor()
 
        content_hash = make_hash(content)
 
        try:
            cursor.execute("""
            INSERT OR IGNORE INTO documents
            (title, content, content_hash, source, category, url, published_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (title, content, content_hash, source, category, url, date))
 
            self.conn.commit()
 
        except Exception as e:
            print("DB Error:", e)