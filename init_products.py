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
    ("KitKat and DairyMilk Bouquet", "Choco Blossom Delight Bouquet", 400, "CB3.jpg"),
    ("Sun Flower Bouquet", "Sunflower Serenity.", 550, "bouquet1.jpg"),
    ("RedVelvet cake with Red roses", "Velvet Roses & Cocoa Dreams", 1060, "combo5.jpg")
]

cursor.executemany('INSERT INTO products (name, description, price, image) VALUES (?, ?, ?, ?)', products)

conn.commit()
print(" Products table created and sample data inserted.")
conn.close()
