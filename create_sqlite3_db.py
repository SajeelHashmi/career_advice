import sqlite3

# Connect to SQLite (creates the database file if it doesn't exist)
conn = sqlite3.connect("telegram_career.db")
cursor = conn.cursor()

# Enable foreign key support
cursor.execute("PRAGMA foreign_keys = ON;")

# Start transaction
conn.execute("BEGIN;")

# Table creation queries
cursor.execute("""
CREATE TABLE chat (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_type INTEGER NOT NULL,
    FOREIGN KEY (chat_type) REFERENCES chat_type(id)
);
""")

cursor.execute("""
CREATE TABLE chat_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT DEFAULT NULL
);
""")

cursor.execute("""
CREATE TABLE message (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER NOT NULL,
    system INTEGER NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chat_id) REFERENCES chat(Id) ON DELETE CASCADE
);
""")



cursor.executemany("""
INSERT INTO chat_type (id, type) VALUES (?, ?);
""", [
    (1, 'career_advice'),
    (2, 'mock_interview')
])



# Commit the transaction
conn.commit()

# Close the connection
conn.close()
