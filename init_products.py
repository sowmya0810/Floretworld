import sqlite3

conn = sqlite3.connect('floret.db')
cursor = conn.cursor()


cursor.execute('DROP TABLE IF EXISTS products')


cursor.execute('''
    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL,
        image TEXT
    )
''')


products = [
    ("Choco Blossom Delight Bouquet", "KitKat and DairyMilk Bouquet", 400, "CB3.jpg"),
    ("SunFlower Serenity", "Sunflower Bouquet", 550, "bouquet1.jpg"),
    ("Velvet Roses & Cocoa Dreams", "RedVelvet cake with Red roses", 1060, "combo5.jpg")
]


cursor.executemany('INSERT INTO products (name, description, price, image) VALUES (?, ?, ?, ?)', products)

conn.commit()
print(" Products table created and sample data inserted.")
conn.close()
