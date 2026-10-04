import sqlite3

def create_db():
    conn = sqlite3.connect("misinfo.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS misinformation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            verdict TEXT,
            source TEXT,
            category TEXT,
            date_added TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_entry(title, content, verdict, source, category, date_added):
    conn = sqlite3.connect("misinfo.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO misinformation (title, content, verdict, source, category, date_added)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, content, verdict, source, category, date_added))
    conn.commit()
    conn.close()

def search_misinformation(query):
    conn = sqlite3.connect("misinfo.db")
    c = conn.cursor()
    c.execute("SELECT * FROM misinformation WHERE content LIKE ?", ('%' + query + '%',))
    results = c.fetchall()
    conn.close()
    return results
