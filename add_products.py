import sqlite3

# Connect to your database
conn = sqlite3.connect('floret.db')
cursor = conn.cursor()

# Insert sample product data
products = [
    ('Roses & Richness Combo', 'products/combos/combo2.jpg', 1060, 3.5),
    ('Sunflower Serenity', 'products/bouquet/bouquet1.jpg', 550, 5),
    ('Crimson Charm Rose', 'products/single/SINGLE1.jpg', 180, 4),
    ('Choco Blossom Delight Bouquet', 'products/chocolate bouquet/CB3.jpg', 400, 4),
]

cursor.executemany('''
    INSERT INTO products (name, image, price, rating)
    VALUES (?, ?, ?, ?)
''', products)

# Commit and close
conn.commit()
conn.close()

print("Products added successfully!")
