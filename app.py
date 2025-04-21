from flask import Flask, render_template, redirect, url_for, session, flash, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_wtf.csrf import CSRFProtect

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'floret.db')

app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = '2003'

def get_db_connection():
    db_path = r"C:/Users/USER/OneDrive/文件/Devopsecommerce/floret.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def get_all_products():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return products

def get_user_by_mailID(mailID):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE mailID = ?", (mailID,)).fetchone()
    conn.close()
    return user

def get_cart_item_count():
    if 'cart' in session:
        return sum(item['quantity'] for item in session['cart'])
    return 0

def get_user_by_mailID_and_password(mailID, password):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE mailID = ?", (mailID,)).fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        return {'id': user['id'], 'mailID': user['mailID']}
    return None


@app.route('/')
def index():
    cart_item_count = get_cart_item_count()
    return render_template('index.html', cart_item_count=cart_item_count)

@app.route('/products')
def products():
    products = get_all_products()
    cart_item_count = get_cart_item_count()
    return render_template('products.html', products=products, cart_item_count=cart_item_count)

@app.route('/about')
def about():
    if 'user_id' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('login'))
    return render_template('about.html')

@app.route('/contact')
def contact():
    if 'user_id' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('login'))
    return render_template('contact.html')

@app.route('/account')
def account():
    if 'user_id' in session:
        flash(f"Welcome {session['user']}! You are logged in.", 'success')
        user = get_user_by_mailID(session['mailID'])
        return render_template('account.html', user=user)
    else:
        flash('Please login first.', 'danger')
        return redirect(url_for('login'))

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        data = request.get_json()
        product_name = data.get('product_name')
        quantity = int(data.get('quantity'))

        if not product_name or quantity <= 0:
            return jsonify({'error': 'Invalid product name or quantity'}), 400

        conn = get_db_connection()
        product = conn.execute("SELECT name, price, image FROM products WHERE name = ?", (product_name,)).fetchone()
        conn.close()

        if not product:
            return jsonify({'error': 'Product not found'}), 404

        cart_item = {
            'name': product['name'],
            'quantity': quantity,
            'price': product['price'],
            'image': product['image']
        }

        cart = session.get('cart', [])
        cart.append(cart_item)
        session['cart'] = cart

        flash(f'{product_name} added to cart with quantity {quantity}', 'success')
        return jsonify({'message': f'{product_name} added to cart with quantity {quantity}'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cart')
def cart():
    cart_item_count = get_cart_item_count()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, price, image FROM cart_items WHERE name = 'Sunflower Bouquet'")
    rows = cursor.fetchall()
    conn.close()

    cart_items = []
    total_price = 0
    for row in rows:
        item = {
            'name': row[0],
            'price': row[1],
            'image': row[2],
            'quantity': 1
        }
        total_price += item['price'] * item['quantity']
        cart_items.append(item)

    tax = round(total_price * 0.05, 2)
    return render_template('cart.html', cart=cart_items, total_price=total_price, tax=tax, cart_item_count=cart_item_count)


@app.route('/update_cart', methods=['POST'])
def update_cart():
    data = request.get_json()
    product_name = data.get('product_name')
    quantity = data.get('quantity')

    cart = session.get('cart', [])
    found = False
    for item in cart:
        if item['name'] == product_name:
            item['quantity'] = quantity
            found = True
            break

    if not found:
        conn = get_db_connection()
        product = conn.execute("SELECT name, price, image FROM products WHERE name = ?", (product_name,)).fetchone()
        conn.close()
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        cart.append({
            'name': product['name'],
            'quantity': quantity,
            'price': product['price'],
            'image': product['image']
        })

    session['cart'] = cart
    total_price = sum(item['price'] * item['quantity'] for item in cart)

    return jsonify({
        'total_price': total_price,
        'cart_item_count': len(cart),
        'price': next(item['price'] for item in cart if item['name'] == product_name),
    })

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    data = request.get_json()
    product_name = data.get('product_name')

    cart = session.get('cart', [])
    cart = [item for item in cart if item['name'] != product_name]
    session['cart'] = cart
    total_price = sum(item['price'] * item['quantity'] for item in cart)

    return jsonify({
        'total_price': total_price,
        'cart_item_count': len(cart),
    })

@app.route('/buy_now/<product_name>', methods=['POST'])
def buy_now(product_name):
    quantity = int(request.form.get('quantity', 1))
    session['cart'] = [{'product_name': product_name, 'quantity': quantity}]
    flash('Proceeding to checkout with selected item.', 'success')
    return redirect(url_for('cart'))

@app.route('/orders')
def view_orders():
    if 'user_id' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('login'))

    conn = get_db_connection()
    orders = conn.execute("SELECT * FROM orders WHERE user_name = ?", (session['user'],)).fetchall()
    conn.close()
    return render_template('orders.html', orders=orders)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mailID = request.form.get('mailID')
        password = request.form.get('password')

        if not mailID or not password:
            flash('Please enter both Mail ID and password.', 'warning')
            return render_template('login.html')

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE mailID = ?", (mailID,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user'] = user['username']
            session['user_id'] = user['id']
            session['mailID'] = user['mailID']
            return redirect(url_for('index'))
        else:
            flash('Invalid Mail ID or password.', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        mailID = request.form['mailID']
        password = request.form['password']
        username = request.form['username']

        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        cursor = conn.cursor()

        existing_user = cursor.execute("SELECT * FROM users WHERE mailID = ?", (mailID,)).fetchone()
        if existing_user:
            flash('This mailID is already registered. Please log in.', 'danger')
            return redirect(url_for('login'))

        cursor.execute("INSERT INTO users (username, mailID, password) VALUES (?, ?, ?)",
                       (username, mailID, hashed_password))
        conn.commit()
        session['user'] = username
        session['user_id'] = cursor.lastrowid
        session['mailID'] = mailID
        conn.close()

        flash('Registration successful. You are now logged in.', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/check_cart')
def check_cart():
    return str(session.get('cart'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
