from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure, random key

# Home redirect
@app.route('/')
def index():
    return redirect(url_for('login'))

# -------------------- LOGIN -------------------- #
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            with sqlite3.connect('floret.db') as conn:
                conn.row_factory = sqlite3.Row
                user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['email'] = user['email']
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid email or password.', 'danger')

        except Exception as e:
            flash(f'Error: {e}', 'danger')

    return render_template('login.html')

# -------------------- REGISTER -------------------- #
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        try:
            with sqlite3.connect('floret.db') as conn:
                conn.execute(
                    'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                    (username, email, hashed_password)
                )
                conn.commit()

            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))

        except sqlite3.IntegrityError:
            flash('Email already registered. Try logging in.', 'danger')

        except sqlite3.OperationalError as e:
            flash(f'Database error: {e}', 'danger')

    return render_template('register.html')

# -------------------- HOME -------------------- #
@app.route('/home')
def home():
    if 'user_id' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('login'))

    return render_template('index.html', email=session['email'])

# -------------------- LOGOUT -------------------- #
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# -------------------- MAIN -------------------- #
if __name__ == '__main__':
    app.run(debug=True)
