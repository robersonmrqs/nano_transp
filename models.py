import sqlite3

def connect_db(db_name = 'nano_transp.db'):
    conn = sqlite3.connect(db_name)
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def users_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def register_user(name, email, username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email, username, password) VALUES (?, ?, ?, ?)', (name, email, username, password))
    conn.commit()
    conn.close()
    user_db_name = f'{username}_nano_transp.db'
    user_conn = connect_db(user_db_name)
    user_conn.close()
    init_user_db(user_db_name)

def get_user_details(username=None, email=None):
    conn = connect_db()
    cursor = conn.cursor()
    if username:
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    elif email:
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def init_user_db(db_name):
    clients_table(db_name)
    incomes_table(db_name)
    expenses_table(db_name)
    fleet_table(db_name)

def clients_table(db_name = 'nano_transp.db'):
    conn = connect_db(db_name)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, address TEXT NOT NULL, email TEXT NOT NULL, phone TEXT NOT NULL, contact TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def incomes_table(db_name = 'nano_transp.db'):
    conn = connect_db(db_name)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS incomes (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, date TEXT NOT NULL, value REAL NOT NULL, client_id INTEGER NOT NULL, paid INTEGER NOT NULL, voucher BLOB, FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE)''')
    conn.commit()
    conn.close()

def expenses_table(db_name = 'nano_transp.db'):
    conn = connect_db(db_name)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, date TEXT NOT NULL, value REAL NOT NULL, source TEXT NOT NULL, voucher BLOB)''')
    conn.commit()
    conn.close()

def fleet_table(db_name = 'nano_transp.db'):
    conn = connect_db(db_name)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS fleet (id INTEGER PRIMARY KEY AUTOINCREMENT, plate TEXT NOT NULL UNIQUE, color TEXT NOT NULL, brand TEXT NOT NULL, model TEXT NOT NULL, initial REAL NOT NULL, final REAL, mileage REAL, obs TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def execute_query(query, params = (), fetchone = False, fetchall = False, db_name = 'nano_transp.db'):
    conn = connect_db(db_name)
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