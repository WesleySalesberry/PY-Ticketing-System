import sqlite3
from tkinter import messagebox


def register_user(conn, username, password):
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, "user"))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists")


def login_user(conn, username, password):
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    return user


def get_all_users(conn):
    c = conn.cursor()
    c.execute('SELECT id, username, role FROM users')
    return c.fetchall()


def update_user_role(conn, user_id, new_role):
    if new_role:
        c = conn.cursor()
        c.execute('UPDATE users SET role = ? WHERE id = ?', (new_role, user_id))
        conn.commit()


def delete_user(conn, user_id):
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
