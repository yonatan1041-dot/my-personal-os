import sqlite3
from datetime import datetime                                                                                                                             def heb(text):
    text = text.replace('(', 'TEMP_L').replace(')', 'TEMP_R')                    text = text.replace('TEMP_L', ')').replace('TEMP_R', '(')                    return text[::-1]                                                                                                                                     def init_db():
    conn = sqlite3.connect('my_private_data.db')                                 cursor = conn.cursor()                                                       cursor.execute('''CREATE TABLE IF NOT EXISTS missions                            (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, goal TEXT,            opt1 TEXT, opt2 TEXT, opt3 TEXT)''')                                     cursor.execute('''CREATE TABLE IF NOT EXISTS journal                             (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, entry TEXT)''')                                                                                conn.commit()                                                                conn.close()                                                             
def add_mission():                                                               print(f"\n--- {heb('משימה חדשה')} ---")                                      goal = input(heb("מה היעד? "))
    o1 = input(heb("אופציה 1: "))                                                o2 = input(heb("אופציה 2: "))                                                o3 = input(heb("אופציה 3: "))                                                conn = sqlite3.connect('my_private_data.db')                                 cursor = conn.cursor()                                                       now = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("INSERT INTO missions (timestamp, goal, opt1, opt2, opt3) VALUES (?, ?, ?, ?, ?)",                                                                        (now, goal, o1, o2, o3))
    conn.commit()                                                                conn.close()
    print(f"\n[V] {heb('נשמר.')}")
                                                                             def add_journal():
    print(f"\n--- {heb('שיחה עם השמיים / יומן מחשבות')} ---")
    entry = input(heb("מה על ליבך ברגע זה? "))                                   conn = sqlite3.connect('my_private_data.db')
    cursor = conn.cursor()                                                       now = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("INSERT INTO journal (timestamp, entry) VALUES (?, ?)", (now, entry))                                                                      conn.commit()                                                                conn.close()                                                                 print(f"\n[V] {heb('המחשבה נשמרה בלב המערכת.')}")
                                                                             def view_data():
    print(f"\n--- {heb('לוח בקרה (1-משימות, 2-יומן)')} ---")                     choice = input(heb("מה תרצה לראות? "))
    conn = sqlite3.connect('my_private_data.db')
    cursor = conn.cursor()                                                       if choice == '1':
        cursor.execute("SELECT id, timestamp, goal FROM missions")                   rows = cursor.fetchall()
        for row in rows: print(f"{row[0]}. [{row[1]}] {row[2][::-1]}")
    elif choice == '2':                                                              cursor.execute("SELECT timestamp, entry FROM journal")
        rows = cursor.fetchall()
        for row in rows: print(f"[{row[0]}] {row[1][::-1]}")
    conn.close()                                                             
def main():
    init_db()
    while True:                                                                      print(f"\n--- {heb('מערכת הפעלה אישית (יונתן)')} ---")
        print(f"1. {heb('הוסף משימה (3 אופציות)')}")
        print(f"2. {heb('שיחה עם השמיים (יומן)')}")
        print(f"3. {heb('צפה בנתונים')}")                                            print(f"4. {heb('מחיקת משימה')}")                                            print(f"5. {heb('יציאה')}")
        choice = input(heb("בחר פעולה: "))
        if choice == '1': add_mission()
        elif choice == '2': add_journal()
        elif choice == '3': view_data(); input(heb("לחץ Enter"))
        elif choice == '4':
            view_data()
            mid = input(heb("מספר משימה למחיקה: "))                                      conn = sqlite3.connect('my_private_data.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM missions WHERE id=?", (mid,))
            conn.commit(); conn.close()                                              elif choice == '5': break                                            if __name__ == "__main__":                                                       main()
