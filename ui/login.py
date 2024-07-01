import customtkinter
import customtkinter as ctk

from tkinter import messagebox
from auth import login_user


class LoginScreen(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        self.username_label = ctk.CTkLabel(self, text="Username")
        self.username_label.pack(pady=5)

        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.pack(pady=5)

        self.password_label = ctk.CTkLabel(self, text="Password")
        self.password_label.pack(pady=5)

        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.pack(pady=5)

        self.register_button = ctk.CTkButton(self, text="Register", command=self.app.create_register_screen)
        self.register_button.pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = login_user(self.app.conn, username, password)

        if user:
            self.app.current_user = user
            self.app.create_main_screen()
        else:
            messagebox.showerror("Error", "Invalid credentials")
