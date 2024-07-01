import customtkinter as ctk
from auth import register_user


class RegisterScreen(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        self.username_label = ctk.CTkLabel(self, text="Username")
        self.username_label.pack(pady=10)

        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.pack(pady=10)

        self.password_label = ctk.CTkLabel(self, text="Password")
        self.password_label.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.pack(pady=10)

        self.register_button = ctk.CTkButton(self, text="Register", command=self.register)
        self.register_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self, text="Back to Login", command=self.app.create_login_screen)
        self.back_button.pack(pady=10)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        register_user(self.app.conn, username, password)
        self.app.create_login_screen()
