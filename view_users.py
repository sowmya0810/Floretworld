import sqlite3
conn = sqlite3.connect('floret.db')
cursor = conn.cursor()
for row in cursor.execute('SELECT * FROM users'):
    print(row)
conn.close()
