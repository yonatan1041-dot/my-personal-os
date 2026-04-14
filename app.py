from flask import Flask, render_template_string, request, redirect, Response, jsonify
import sqlite3
from functools import wraps

app = Flask(__name__)

# --- הגדרות אבטחה ---
USER = "yonatan"  
PASS = "1234"     # תזכור לשנות את זה למה שבחרת

def check_auth(username, password):
    return username == USER and password == PASS

def authenticate():
    return Response(
    'נא להזין שם משתמש וסיסמה', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
# --------------------

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
@requires_auth
def home():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM messages ORDER BY id DESC")
    messages = cursor.fetchall()
    conn.close()
    
    html = '''
    <!DOCTYPE html>
    <html lang="he" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Yonatan's OS</title>
        <style>
            body { background-color: #0f172a; color: #f8fafc; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; min-height: 100vh; margin: 0; padding: 20px; }
            .container { background-color: #1e293b; padding: 2rem; border-radius: 1rem; width: 90%; max-width: 500px; border: 1px solid #334155; }
            h1 { color: #38bdf8; text-align: center; }
            input[type="text"] { width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #334155; background: #0f172a; color: white; margin-bottom: 10px; box-sizing: border-box; }
            button { width: 100%; padding: 12px; background-color: #38bdf8; color: #0f172a; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }
            ul { list-style: none; padding: 0; margin-top: 20px; }
            li { background: #334155; padding: 12px; margin-bottom: 8px; border-radius: 8px; border-right: 4px solid #38bdf8; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>OS Terminal</h1>
            <form action="/add" method="post">
                <input type="text" name="message" placeholder="שלח פקודה או מחשבה..." required>
                <button type="submit">שלח</button>
            </form>
            <ul>
                {% for msg in messages %}
                    <li>{{ msg[0] }}</li>
                {% endfor %}
            </ul>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, messages=messages)

# --- ה-API שמקבל נתונים מטרמקס ---
@app.route('/api/send', methods=['POST'])
def api_send():
    data = request.json
    message = data.get('message')
    api_key = data.get('api_key')
    
    # בדיקת אבטחה בסיסית ל-API
    if api_key == "my_secret_key" and message:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (content) VALUES (?)", (message,))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error"}), 401

@app.route('/add', methods=['POST'])
@requires_auth
def add_message():
    message = request.form.get('message')
    if message:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (content) VALUES (?)", (message,))
        conn.commit()
        conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
