import sqlite3
from pprint import pprint

def show_rows(limit=20):
    conn = sqlite3.connect("misinfo.db")
    c = conn.cursor()
    c.execute("SELECT id, title, verdict, source, category, date_added FROM misinformation ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    pprint(rows)

if __name__ == "__main__":
    show_rows(50)