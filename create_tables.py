import sqlite3
 
conn = sqlite3.connect("intel.db")

cursor = conn.cursor()
 
cursor.execute("""

CREATE TABLE IF NOT EXISTS strategic_signals (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
 
    document_id INTEGER,
 
    sentiment TEXT,

    sentiment_score REAL,
 
    risks TEXT,

    opportunities TEXT,

    trends TEXT,
 
    keywords TEXT,

    entities TEXT,
 
    impact TEXT,
 
    FOREIGN KEY(document_id)

        REFERENCES documents(id)

)

""")
 
conn.commit()

conn.close()
 
print("Strategic Signals table created")
 