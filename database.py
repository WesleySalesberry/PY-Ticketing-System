import sqlite3
from tkinter import messagebox


def create_connection():
    conn = sqlite3.connect('ticketing_system.db')
    return conn


def setup_database(conn):
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS issues (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        severity TEXT,
        tech_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (tech_id) REFERENCES users(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY,
        issue_id INTEGER,
        tech_id INTEGER,
        note TEXT NOT NULL,
        FOREIGN KEY (issue_id) REFERENCES issues(id),
        FOREIGN KEY (tech_id) REFERENCES users(id)
    )''')

    conn.commit()

    # Check if admin user exists, if not create it
    c.execute('SELECT * FROM users WHERE username = ?', ('admin',))
    if not c.fetchone():
        c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', ('admin', '123456', 'admin'))
        conn.commit()
