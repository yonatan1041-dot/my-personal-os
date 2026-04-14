from flask import Flask, render_template_string, request, redirect, Response, jsonify
import sqlite3
from functools import wraps

app = Flask(__name__)

USER = "yonatan"
PASS = "1234" # תזכור לשנות למה שבחרת

def check_auth(username, password):
    return username == USER and password == PASS

def authenticate():
    return Response('Login Required', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password): return authenticate()
        return f(*args, **kwargs)
    return decorated

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS commands (id INTEGER PRIMARY KEY AUTOINCREMENT, cmd TEXT, status TEXT)')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
@requires_auth
def home():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM messages ORDER BY id DESC LIMIT 10")
    messages = cursor.fetchall()
    conn.close()
    
    # שליפת הסטטוס האחרון עבור הווידג'טים
    last_status = messages[0][0] if messages else "No data"
    
    html = '''
    <!DOCTYPE html>
    <html lang="he" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Yonatan's Dashboard</title>
        <style>
            body { background: #0b0f19; color: #e2e8f0; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; max-width: 1000px; margin: auto; }
            .card { background: #161e2d; padding: 20px; border-radius: 15px; border: 1px solid #1e293b; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
            h2 { color: #38bdf8; margin-top: 0; font-size: 1.2rem; }
            .status-val { font-size: 1.5rem; font-weight: bold; color: #10b981; }
            input, button { width: 100%; padding: 12px; margin-top: 10px; border-radius: 8px; border: none; box-sizing: border-box; }
            input { background: #0b0f19; color: white; border: 1px solid #334155; }
            button { background: #38bdf8; color: #0b0f19; font-weight: bold; cursor: pointer; transition: 0.3s; }
            button:hover { background: #0ea5e9; }
            .log-item { background: #1e293b; padding: 10px; margin-top: 8px; border-radius: 6px; font-size: 0.9rem; border-right: 3px solid #38bdf8; }
        </style>
    </head>
    <body>
        <h1 style="text-align:center; color:#38bdf8;">Yonatan's OS Terminal</h1>
        <div class="grid">
            <div class="card">
                <h2>מצב מכשיר (Termux)</h2>
                <div class="status-val">{{ last_status }}</div>
            </div>
            <div class="card">
                <h2>שלח פקודה לטרמקס</h2>
                <form action="/send_cmd" method="post">
                    <input type="text" name="cmd" placeholder="למשל: say hello" required>
                    <button type="submit">בצע פקודה</button>
                </form>
            </div>
            <div class="card" style="grid-column: 1 / -1;">
                <h2>לוג הודעות אחרונות</h2>
                {% for msg in messages %}
                    <div class="log-item">{{ msg[0] }}</div>
                {% endfor %}
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, messages=messages, last_status=last_status)

@app.route('/send_cmd', methods=['POST'])
@requires_auth
def send_cmd():
    cmd = request.form.get('cmd')
    if cmd:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO commands (cmd, status) VALUES (?, 'pending')", (cmd,))
        conn.commit()
        conn.close()
    return redirect('/')

@app.route('/api/get_cmd', methods=['GET'])
def get_cmd():
    # טרמקס ימשוך פקודות מכאן
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, cmd FROM commands WHERE status = 'pending' ORDER BY id ASC LIMIT 1")
    row = cursor.fetchone()
    if row:
        cursor.execute("UPDATE commands SET status = 'done' WHERE id = ?", (row[0],))
        conn.commit()
        conn.close()
        return jsonify({"id": row[0], "cmd": row[1]})
    conn.close()
    return jsonify({"cmd": None})

@app.route('/api/send', methods=['POST'])
def api_send():
    data = request.json
    if data.get('api_key') == "my_secret_key":
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (content) VALUES (?)", (data.get('message'),))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error"}), 401

if __name__ == '__main__':
    app.run(debug=True)

