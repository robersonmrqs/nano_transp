import sqlite3

def connect_db():
    conn = sqlite3.connect('nano_transp.db')
    return conn

def users_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def get_user_details(username = None, email = None):
    conn = connect_db()
    cursor = conn.cursor()
    if username and email:
        cursor.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email))
    elif username:
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    elif email:
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    else:
        return None
    user_found = cursor.fetchone()
    conn.close()
    return user_found

def register_user(name, email, username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email, username, password) VALUES (?, ?, ?, ?)', (name, email, username, password))
    conn.commit()
    conn.close()