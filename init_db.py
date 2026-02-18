import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS announcements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    author TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
INSERT INTO announcements (title, content, author)
VALUES
    ('Welcome to the Season', 'First team meeting Friday', 'john_deere' ),
    ('Practice Moved', 'Practice is moved from 4pm to 6pm tonight.', 'tiger_woods')
""")

conn.commit()
conn.close()
