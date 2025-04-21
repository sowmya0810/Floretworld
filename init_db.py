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

# Insert multiple test users
users = [
    ("sowmya", "sowmya@gmail.com", generate_password_hash("123")),
    ("priya", "priya10@gamil.com", generate_password_hash("priya")),
    ("harshu", "harshu30@gamil.com", generate_password_hash("harshu")),
    ("hari", "harish22@example.com", generate_password_hash("hari"))
]

cursor.executemany("INSERT INTO users (username, mailID, password) VALUES (?, ?, ?)", users)

conn.commit()
print("Table created and multiple test users inserted.")
conn.close()
