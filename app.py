from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import pandas as pd
from functools import wraps

app = Flask(__name__)
app.secret_key = "secret"
DB_NAME = "inventory.db"

# ----------------------
# Database setup
# ----------------------
def create_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT,
                    stock INTEGER NOT NULL,
                    price REAL NOT NULL
                )''')
    conn.commit()
    conn.close()

def create_user_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )''')
    # default admin
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", 
              ("admin", "password"))
    conn.commit()
    conn.close()

# ----------------------
# Inventory functions
# ----------------------
def get_inventory_df():
    conn = sqlite3.connect(DB_NAME)
    try:
        df = pd.read_sql_query("SELECT * FROM products", conn)
        expected_cols = ['id', 'name', 'category', 'stock', 'price']
        for col in expected_cols:
            if col not in df.columns:
                df[col] = 0 if col in ['stock', 'price'] else ''
    except Exception:
        df = pd.DataFrame(columns=['id', 'name', 'category', 'stock', 'price'])
    finally:
        conn.close()
    return df

def add_product(name, stock, price, category="General"):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO products (name, category, stock, price) VALUES (?, ?, ?, ?)",
              (name, category, stock, price))
    conn.commit()
    conn.close()

def delete_product(pid):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id=?", (pid,))
    conn.commit()
    conn.close()

# ----------------------
# Login system
# ----------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash("Please login first", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['user'] = username
            flash(f"Welcome, {username}!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for('login'))
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully", "success")
    return redirect(url_for('login'))

# ----------------------
# Routes
# ----------------------
@app.route('/')
@login_required
def index():
    search_query = request.args.get('q', '').lower()
    df = get_inventory_df()

    if search_query:
        df = df[df['name'].str.lower().str.contains(search_query) |
                df['category'].str.lower().str.contains(search_query)]

    products = df.to_dict(orient='records')
    total_products = len(df)
    low_stock = len(df[df['stock'] < 10])
    inventory_value = df['stock'].sum() * df['price'].mean() if not df.empty else 0
    return render_template("index.html", products=products, total_products=total_products,
                           low_stock=low_stock, inventory_value=inventory_value, q=search_query)

@app.route('/add', methods=['POST'])
@login_required
def add():
    name = request.form['pname']
    stock = int(request.form['pstock'])
    price = float(request.form['pprice'])
    add_product(name, stock, price)
    flash("Product added successfully!", "success")
    return redirect(url_for('index'))

@app.route('/delete/<int:pid>')
@login_required
def delete(pid):
    delete_product(pid)
    flash("Product deleted successfully!", "success")
    return redirect(url_for('index'))

@app.route('/export_csv')
@login_required
def export_csv():
    df = get_inventory_df()
    df.to_csv("inventory_export.csv", index=False)
    flash("Inventory exported to CSV!", "success")
    return redirect(url_for('index'))

# ----------------------
# Run app
# ----------------------
if __name__ == "__main__":
    create_db()
    create_user_db()
    app.run(debug=True)
