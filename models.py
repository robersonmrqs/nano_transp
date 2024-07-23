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

def clients_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, adress TEXT NOT NULL, email REAL NOT NULL, phone TEXT NOT NULL, contact TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def incomes_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS incomes (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, data TEXT NOT NULL, value REAL NOT NULL, client_id INTEGER NOT NULL, paid INTEGER NOT NULL, voucher BLOB, FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE)''')
    conn.commit()
    conn.close()

def expenses_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, data TEXT NOT NULL, value REAL NOT NULL, source TEXT NOT NULL, voucher BLOB)''')
    conn.commit()
    conn.close()

def execute_query(query, params = (), fetchone = False, fetchall = False):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = None
    if fetchone:
        result = cursor.fetchone()
    elif fetchall:
        result = cursor.fetchall()
    else:
        conn.commit()
    conn.close()
    return result