import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('floret.db')
cursor = conn.cursor()

# ❗ Drop existing table (this will delete all existing user data)
cursor.execute('DROP TABLE IF EXISTS users')

# ✅ Create new table with username
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# ✅ Insert user
username = "sowmya"
email = "sowmya@gmail.com"
password = generate_password_hash("123")

cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))

conn.commit()
print("✅ User added and table created.")
conn.close()
