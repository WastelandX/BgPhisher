from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
import hashlib
import sqlite3
import os
from datetime import datetime, timedelta
import jwt
import json

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()
app.config['DATABASE'] = 'users.db'
app.config['JWT_SECRET'] = 'your-secret-key-change-in-production'
app.config['SESSION_TYPE'] = 'filesystem'

# ========== DATABASE SETUP ==========
def init_db():
    """Initialize database with users table"""
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  password_hash TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  last_login TIMESTAMP,
                  is_active BOOLEAN DEFAULT 1)''')
    
    # Create sessions table for persistent login
    c.execute('''CREATE TABLE IF NOT EXISTS user_sessions
                 (session_id TEXT PRIMARY KEY,
                  user_id INTEGER,
                  expires_at TIMESTAMP,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    # Insert a demo user if none exists
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        demo_pass = hashlib.sha256('demo123'.encode()).hexdigest()
        c.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                  ('demo', 'demo@example.com', demo_pass))
    
    conn.commit()
    conn.close()

# ========== HELPER FUNCTIONS ==========
def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, stored_hash):
    """Verify password against stored hash"""
    return hash_password(password) == stored_hash

def create_session_token(user_id):
    """Create JWT session token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, app.config['JWT_SECRET'], algorithm='HS256')

def verify_session_token(token):
    """Verify JWT session token"""
    try:
        payload = jwt.decode(token, app.config['JWT_SECRET'], algorithms=['HS256'])
        return payload['user_id']
    except:
        return None

# ========== DECORATORS ==========
def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def json_response(f):
    """Decorator for JSON API responses"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            if isinstance(result, tuple):
                data, status = result
            else:
                data, status = result, 200
            return jsonify({'success': True, 'data': data}), status
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400
    return decorated_function

# ========== ROUTES ==========
@app.route('/')
def index():
    """Home page - redirect to login or dashboard"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page with AJAX support"""
    if request.method == 'POST':
        if request.is_json:
            # AJAX login
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
        else:
            # Form submission
            username = request.form.get('username')
            password = request.form.get('password')
        
        # Validate input
        if not username or not password:
            if request.is_json:
                return jsonify({'success': False, 'error': 'Missing credentials'}), 400
            flash('Please enter username and password', 'error')
            return redirect(url_for('login'))
        
        # Check user in database
        conn = sqlite3.connect(app.config['DATABASE'])
        c = conn.cursor()
        c.execute("SELECT id, password_hash FROM users WHERE username = ? AND is_active = 1", (username,))
        user = c.fetchone()
        
        if user and verify_password(password, user[1]):
            user_id = user[0]
            session['user_id'] = user_id
            session['username'] = username
            
            # Update last login
            c.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?", (user_id,))
            conn.commit()
            
            # Create session token for API
            token = create_session_token(user_id)
            
            if request.is_json:
                return jsonify({
                    'success': True,
                    'redirect': url_for('dashboard'),
                    'token': token,
                    'user': {'id': user_id, 'username': username}
                }), 200
            else:
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
        else:
            if request.is_json:
                return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
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
            return redirect(url_for('register'))
        
        # Check if user exists
        conn = sqlite3.connect(app.config['DATABASE'])
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
        if c.fetchone():
            flash('Username or email already exists', 'error')
            return redirect(url_for('register'))
        
        # Create user
        password_hash = hash_password(password)
        c.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                  (username, email, password_hash))
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard after login"""
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute("SELECT username, email, created_at, last_login FROM users WHERE id = ?", 
              (session['user_id'],))
    user = c.fetchone()
    conn.close()
    
    return render_template('dashboard.html', 
                         username=user[0],
                         email=user[1],
                         created=user[2],
                         last_login=user[3])

@app.route('/api/check-username/<username>')
def check_username(username):
    """API endpoint to check username availability"""
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    exists = c.fetchone() is not None
    conn.close()
    
    return jsonify({'available': not exists, 'username': username})

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/api/me')
@json_response
def get_current_user():
    """API endpoint to get current user info"""
    if 'user_id' not in session:
        return {'authenticated': False}, 401
    
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute("SELECT id, username, email FROM users WHERE id = ?", (session['user_id'],))
    user = c.fetchone()
    conn.close()
    
    return {
        'authenticated': True,
        'user': {
            'id': user[0],
            'username': user[1],
            'email': user[2]
        }
    }

# ========== ERROR HANDLERS ==========
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

# ========== MAIN ==========
if __name__ == '__main__':
    init_db()  # Initialize database on startup
    print("=" * 50)
    print("BLOCKMAN GO Login System")
    print("=" * 50)
    print("Demo Credentials:")
    print("  Username: demo")
    print("  Password: demo123")
    print("=" * 50)
    print("Server running at: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)