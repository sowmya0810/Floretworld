import sqlite3

def create_orders_table():
    conn = sqlite3.connect('floret.db')
    cursor = conn.cursor()

    # Create the orders table
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        product_name TEXT,
                        quantity INTEGER,
                        price REAL,
                        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                      )''')

    # Insert a sample order for testing purposes
    cursor.execute('''INSERT INTO orders (user_id, product_name, quantity, price)
                      VALUES (?, ?, ?, ?)''', (1, 'Sample Product', 1, 29.99))

    conn.commit()
    conn.close()
    print("Orders table created and sample data inserted.")
