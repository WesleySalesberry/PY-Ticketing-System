import customtkinter as ctk
import tkinter as tk
from tkinter import simpledialog, messagebox
from auth import get_all_users, update_user_role, delete_user


class AdminUsersScreen(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        self.setup_layout()

    def setup_layout(self):
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.user_frame = ctk.CTkFrame(self)
        self.user_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.refresh_users_button = ctk.CTkButton(self.button_frame, text="Refresh Users", command=self.load_users)
        self.refresh_users_button.pack(pady=10)

        self.change_role_button = ctk.CTkButton(self.button_frame, text="Change Role", command=self.change_role)
        self.change_role_button.pack(pady=10)

        self.delete_user_button = ctk.CTkButton(self.button_frame, text="Delete User", command=self.delete_user)
        self.delete_user_button.pack(pady=10)

        self.user_listbox = tk.Listbox(self.user_frame)
        self.user_listbox.pack(pady=10, fill="both", expand=True)

        self.load_users()

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
