from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'pomp')

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'test'),
    'charset': "latin1"
}

# Establish database connection
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Initialize database tables
def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Creating tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Employee (
        EmpID INT AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(100),
        Email VARCHAR(100),
        PhoneNo VARCHAR(15),
        Position VARCHAR(50),
        Salary FLOAT,
        JoinDate DATE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Customer (
        CusID INT AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(100),
        Email VARCHAR(100),
        PhoneNo VARCHAR(15)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Product (
        ProdID INT AUTO_INCREMENT PRIMARY KEY,
        ProductName VARCHAR(100),
        Category VARCHAR(100),
        Price FLOAT,
        ExpDate DATE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Supplier (
        SuppID INT AUTO_INCREMENT PRIMARY KEY,
        SuppName VARCHAR(100),
        Email VARCHAR(100),
        PhoneNo VARCHAR(15),
        Address TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Orders (
        OrderID INT AUTO_INCREMENT PRIMARY KEY,
        OrderDate DATE,
        TotalAmount FLOAT,
        CusID INT,
        FOREIGN KEY (CusID) REFERENCES Customer(CusID)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS OrderItem (
        ItemID INT AUTO_INCREMENT PRIMARY KEY,
        OrderID INT,
        ProdID INT,
        Quantity INT,
        Price FLOAT,
        FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
        FOREIGN KEY (ProdID) REFERENCES Product(ProdID)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Payment (
        PaymentID INT AUTO_INCREMENT PRIMARY KEY,
        PaymentMethod VARCHAR(50),
        Amount FLOAT,
        PaymentDate DATE,
        OrderID INT,
        FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()


# User authentication (login/logout)
users = {
    "admin": generate_password_hash("admin"),
    "user": generate_password_hash("user")
}

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username in users and check_password_hash(users[username], password):
        session['user'] = username
        return redirect(url_for('dashboard'))
    flash('Invalid credentials', 'danger')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html')

# CRUD operations
@app.route('/<table>/manage', methods=['GET', 'POST'])
def manage_records(table):
    if 'user' not in session:
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SHOW COLUMNS FROM {table}")
    fields = [col['Field'] for col in cursor.fetchall()]

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            values = tuple(request.form.get(field) for field in fields[1:])
            placeholders = ', '.join(['%s'] * len(values))
            query = f"INSERT INTO {table} ({', '.join(fields[1:])}) VALUES ({placeholders})"
            cursor.execute(query, values)
        elif action == 'update':
            record_id = request.form.get(fields[0])
            values = tuple(request.form.get(field) for field in fields[1:]) + (record_id,)
            set_clause = ', '.join([f"{field}=%s" for field in fields[1:]])
            query = f"UPDATE {table} SET {set_clause} WHERE {fields[0]}=%s"
            cursor.execute(query, values)
        elif action == 'delete':
            record_id = request.form.get(fields[0])
            query = f"DELETE FROM {table} WHERE {fields[0]}=%s"
            cursor.execute(query, (record_id,))
        conn.commit()

    cursor.execute(f"SELECT * FROM {table}")
    records = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('manage.html', table=table, fields=fields, records=records)

# Export data to CSV
@app.route('/export/<table>')
def export_to_csv(table):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    csv_file = f"{table}_data.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([i[0] for i in cursor.description])  # Header row
        writer.writerows(rows)

    return jsonify({'message': f"Data exported to {csv_file}"})



if __name__ == '__main__':
    # Initialize the database (if required)
    initialize_database()
    
    # Get the port from the environment variable, or default to 5000
    port = int(os.environ.get("PORT", 5000)) 
    
    # Run the Flask app with host set to 0.0.0.0 (to be accessible on Render)
    app.run(host="0.0.0.0", port=port, debug=False)
