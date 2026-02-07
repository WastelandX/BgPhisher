"""
BLOCKMAN GO - Complete Login System
Simple Flask backend with SQLite database
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
import sqlite3
import os
import hashlib

# ========== FLASK APP SETUP ==========
app = Flask(__name__)
app.secret_key = os.urandom(24).hex()  # Random secret key for sessions
DATABASE = 'users.db'

# ========== DATABASE FUNCTIONS ==========
def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

def init_database():
    """Initialize the database with required tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create demo user if doesn't exist
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'demo'")
    if cursor.fetchone()[0] == 0:
        demo_password = hash_password('demo123')
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            ('demo', 'demo@example.com', demo_password)
        )
        print("✓ Demo user created: username='demo', password='demo123'")
    
    conn.commit()
    conn.close()
    print("✓ Database initialized successfully")

# ========== HELPER FUNCTIONS ==========
def hash_password(password):
    """Hash password for storage"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password, hashed):
    """Verify password against hash"""
    return hash_password(password) == hashed

def login_required(f):
    """Decorator to protect routes that require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ========== ROUTES ==========
@app.route('/')
def home():
    """Home page - redirect to login or dashboard"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Validate input
        if not username or not password:
            flash('Please enter both username and password', 'error')
            return render_template('login.html')
        
        # Check user in database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, password FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password(password, user['password']):
            # Login successful
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'Welcome back, {user["username"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
            return render_template('login.html')
    
    # GET request - show login page
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validate input
        errors = []
        if len(username) < 3:
            errors.append('Username must be at least 3 characters')
        if len(password) < 6:
            errors.append('Password must be at least 6 characters')
        if password != confirm_password:
            errors.append('Passwords do not match')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html')
        
        # Check if user already exists
        conn = get_db()
        cursor = conn.cursor()
        
        # Check username
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            flash('Username already exists', 'error')
            conn.close()
            return render_template('register.html')
        
        # Check email
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            flash('Email already registered', 'error')
            conn.close()
            return render_template('register.html')
        
        # Create new user
        hashed_password = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed_password)
        )
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    # GET request - show registration page
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard after login"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, email, created_at FROM users WHERE id = ?",
        (session['user_id'],)
    )
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return render_template('dashboard.html',
                             username=user['username'],
                             email=user['email'],
                             joined_date=user['created_at'])
    else:
        flash('User not found', 'error')
        return redirect(url_for('logout'))

@app.route('/logout')
def logout():
    """Logout user and clear session"""
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/check-username/<username>')
def check_username(username):
    """API endpoint to check username availability"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    return jsonify({
        'available': user is None,
        'username': username
    })

# ========== ERROR HANDLERS ==========
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

# ========== START APPLICATION ==========
if __name__ == '__main__':
    # Initialize database
    init_database()
    
    # Print startup information
    print("\n" + "="*50)
    print("BLOCKMAN GO - Login System")
    print("="*50)
    print("Server running at: http://127.0.0.1:5000")
    print("Demo credentials:")
    print("  Username: demo")
    print("  Password: demo123")
    print("="*50 + "\n")
    
    # Run the app
    app.run(debug=True, host='127.0.0.1', port=5000)