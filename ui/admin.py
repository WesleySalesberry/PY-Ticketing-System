import customtkinter as ctk
import tkinter as tk
from tkinter import simpledialog, messagebox
from auth import get_all_users, update_user_role, delete_user


class AdminScreen(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        # self.back_button = ctk.CTkButton(self, text="Back", command=self.app.create_main_screen)
        # self.back_button.pack(pady=10)

        self.issue_listbox = tk.Listbox(self)
        self.issue_listbox.pack(pady=10, fill="both", expand=True)

        self.refresh_button = ctk.CTkButton(self, text="Refresh Issues", command=self.load_admin_issues)
        self.refresh_button.pack(pady=10)

        self.sort_by_user_button = ctk.CTkButton(self, text="Sort by User",
                                                 command=lambda: self.load_admin_issues(sort_by="user"))
        self.sort_by_user_button.pack(pady=10)

        self.sort_by_severity_button = ctk.CTkButton(self, text="Sort by Severity",
                                                     command=lambda: self.load_admin_issues(sort_by="severity"))
        self.sort_by_severity_button.pack(pady=10)

        self.load_admin_issues()

        self.user_listbox = tk.Listbox(self)
        self.user_listbox.pack(pady=10, fill="both", expand=True)

        self.refresh_users_button = ctk.CTkButton(self, text="Refresh Users", command=self.load_users)
        self.refresh_users_button.pack(pady=10)

        self.change_role_button = ctk.CTkButton(self, text="Change Role", command=self.change_role)
        self.change_role_button.pack(pady=10)

        self.delete_user_button = ctk.CTkButton(self, text="Delete User", command=self.delete_user)
        self.delete_user_button.pack(pady=10)

        self.load_users()

    def load_admin_issues(self, sort_by=None):
        self.issue_listbox.delete(0, tk.END)
        c = self.app.conn.cursor()

        if sort_by == "user":
            c.execute('SELECT * FROM issues ORDER BY user_id')
        elif sort_by == "severity":
            c.execute('SELECT * FROM issues ORDER BY severity')
        else:
            c.execute('SELECT * FROM issues')

        issues = c.fetchall()
        for issue in issues:
            self.issue_listbox.insert(tk.END, f"{issue[0]}: {issue[2]} - {issue[3]} (Severity: {issue[4]})")

    def load_users(self):
        self.user_listbox.delete(0, tk.END)
        users = get_all_users(self.app.conn)
        for user in users:
            self.user_listbox.insert(tk.END, f"{user[0]}: {user[1]} - {user[2]}")

    def change_role(self):
        selected_user = self.user_listbox.get(tk.ACTIVE)
        if not selected_user:
            messagebox.showerror("Error", "No user selected")
            return

        user_id = int(selected_user.split(':')[0])

        new_role = simpledialog.askstring("New Role", "Enter new role (user/tech/admin):")
        if new_role:
            update_user_role(self.app.conn, user_id, new_role)
            self.load_users()
        else:
            messagebox.showinfo("Info", "Role update cancelled")

    def delete_user(self):
        selected_user = self.user_listbox.get(tk.ACTIVE)
        if not selected_user:
            messagebox.showerror("Error", "No user selected")
            return

        user_id = int(selected_user.split(':')[0])
        confirmation = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this user?")
        if confirmation:
            delete_user(self.app.conn, user_id)
            self.load_users()
            messagebox.showinfo("Success", "User deleted successfully")
        else:
            messagebox.showinfo("Info", "User deletion cancelled")
