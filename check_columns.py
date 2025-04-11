import sqlite3

conn = sqlite3.connect('floret.db')
cursor = conn.cursor()

# Check table structure
cursor.execute("PRAGMA table_info(users)")
columns = cursor.fetchall()

print("Columns in 'users' table:")
for column in columns:
    print(f"{column[1]} ({column[2]})")

conn.close()
