import sqlite3

print("HELLO TEST RUNNING")

conn = sqlite3.connect("nepse.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS market_leaders (
    date TEXT,
    symbol TEXT,
    category TEXT,
    rank INTEGER,
    value TEXT
)
""")

conn.commit()
conn.close()

print("Database ready")