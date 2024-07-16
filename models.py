import sqlite3

def create_conn():
    conn = sqlite3.connect('nano_transp.db')
    return conn

def users_table(conn):
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL)')
    conn.commit()

if __name__ == '__main__':
    conn = create_conn()
    users_table(conn)