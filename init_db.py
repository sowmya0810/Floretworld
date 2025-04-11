import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('floret.db')
cursor = conn.cursor()

# Drop and recreate the table
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        mailID TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

# Insert a test user
username = "sowmya"
mailID = "sowmya@gmail.com"
password = generate_password_hash("123")

cursor.execute("INSERT INTO users (username, mailID, password) VALUES (?, ?, ?)", (username, mailID, password))

conn.commit()
print("✅ Table created and test user inserted.")
conn.close()
