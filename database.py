# database.py
import sqlite3

def init_db():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT, email TEXT, phone TEXT, course TEXT, course_duration TEXT, message TEXT)''')
    conn.commit()
    conn.close()

def save_user(name, email, phone, course='', course_duration='', message=''):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # Check if the user already exists (based on email)
    c.execute("SELECT id FROM users WHERE email = ?", (email,))
    result = c.fetchone()
    if result:
        # Update existing user with new message (append if message exists)
        c.execute("UPDATE users SET message = message || '\n' || ? WHERE email = ?", (message, email))
    else:
        # Insert new user
        c.execute("INSERT INTO users (name, email, phone, course, course_duration, message) VALUES (?, ?, ?, ?, ?, ?)",
                  (name, email, phone, course, course_duration, message))
    conn.commit()
    conn.close()