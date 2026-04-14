from flask import Flask, render_template_string, request, redirect
import sqlite3
import brain

app = Flask(__name__)

# יצירת בסיס הנתונים
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
    <html>
        <head><title>My Personal OS</title></head>
        <body>
            <h1>Welcome to My Personal OS</h1>
            <form action="/add" method="post">
                <input type="text" name="message" placeholder="Type something...">
                <button type="submit">Send</button>
            </form>
            <ul>
                {% for msg in messages %}
                    <li>{{ msg[0] }}</li>
                {% endfor %}
            </ul>
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
