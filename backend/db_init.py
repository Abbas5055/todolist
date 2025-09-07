# Initializes the SQLite database with the todos table.
import sqlite3, os
db_path = os.path.join(os.path.dirname(__file__), "todos.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        done INTEGER NOT NULL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
''')
conn.commit()
conn.close()
print("Initialized database at", db_path)
