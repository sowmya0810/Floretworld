from flask import Flask, render_template, redirect, url_for, session, flash, request
import sqlite3

app = Flask(__name__)
app.secret_key = '2003'

# Home page route
@app.route('/')
def index():
    print("Session contents:", session)
    if 'user_id' in session:
        return render_template('index.html', username=session.get('user'))
    else:
        flash('Please log in to continue.', 'warning')
        return redirect(url_for('login'))

# Products page route
@app.route('/products')
def products():
    if 'user_id' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('login'))
    return render_template('products.html')

# About page
@app.route('/about')
def about():
    if 'user_id' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('login'))
    return render_template('about.html')

# Contact page
@app.route('/contact')
def contact():
    if 'user_id' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('login'))
    return render_template('contact.html')

# Cart page
@app.route('/cart')
def cart():
    cart_items = []
    total = 0

    if 'cart' in session:
        with sqlite3.connect('floret.db') as conn:
            conn.row_factory = sqlite3.Row
            for product_name in session['cart']:
                product = conn.execute("SELECT * FROM products WHERE name = ?", (product_name,)).fetchone()
                if product:
                    product_dict = dict(product)
                    product_dict['quantity'] = session['cart'][product_name]
                    product_dict['subtotal'] = product_dict['price'] * product_dict['quantity']

                    cart_items.append(product_dict)
                    total += product_dict['subtotal']

    return render_template('cart.html', cart_items=cart_items, total=total)

# Account page
@app.route('/account')
def account():
    if 'user_id' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('login'))
    return render_template('account.html')

from werkzeug.security import check_password_hash

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mailID = request.form['mailID']
        password = request.form['password']

        conn = sqlite3.connect('floret.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        user = cursor.execute("SELECT * FROM users WHERE mailID = ?", (mailID,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user'] = user['username']
            session['user_id'] = user['id']
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/add_to_cart/<product_name>', methods=['POST'])
def add_to_cart(product_name):
    quantity = int(request.form.get('quantity', 1))
    if 'cart' not in session:
        session['cart'] = []

    # Check if product already in cart
    for item in session['cart']:
        if item['product_name'] == product_name:
            item['quantity'] += quantity
            break
    else:
        session['cart'].append({'product_name': product_name, 'quantity': quantity})

    session.modified = True
    return redirect(request.referrer or url_for('index'))


@app.route('/buy_now/<product_name>', methods=['POST'])
def buy_now(product_name):
    session['cart'] = {}  
    session['cart'][product_name] = 1
    flash('Redirecting to checkout with this item.', 'success')
    return redirect(url_for('cart'))

from werkzeug.security import generate_password_hash

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        mailID = request.form['mailID']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        with sqlite3.connect('floret.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (mailID, password) VALUES (?, ?)", (mailID, hashed_password))
            conn.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, use_debugger=True)
