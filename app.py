from flask import Flask, render_template_string, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
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
            body {
                background-color: #0f172a;
                color: #f8fafc;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                margin: 0;
            }
            .container {
                background-color: #1e293b;
                padding: 2rem;
                border-radius: 1rem;
                box-shadow: 0 10px 25px rgba(0,0,0,0.5);
                width: 90%;
                max-width: 500px;
                border: 1px solid #334155;
            }
            h1 { color: #38bdf8; text-align: center; }
            input[type="text"] {
                width: 100%;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #334155;
                background: #0f172a;
                color: white;
                margin-bottom: 10px;
                box-sizing: border-box;
            }
            button {
                width: 100%;
                padding: 10px;
                background-color: #38bdf8;
                color: #0f172a;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                cursor: pointer;
            }
            button:hover { background-color: #0ea5e9; }
            ul { list-style: none; padding: 0; margin-top: 20px; }
            li {
                background: #334155;
                padding: 10px;
                margin-bottom: 5px;
                border-radius: 5px;
                border-right: 4px solid #38bdf8;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Yonatan's Personal OS</h1>
            <form action="/add" method="post">
                <input type="text" name="message" placeholder="מה המחשבה שלך עכשיו?" required>
                <button type="submit">שלח למערכת</button>
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

@app.route('/add', methods=['POST'])
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
