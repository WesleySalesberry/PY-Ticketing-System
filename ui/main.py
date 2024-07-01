import customtkinter as ctk
from ui.login import LoginScreen
from ui.register import RegisterScreen
from ui.user import UserScreen
from ui.tech import TechScreen
from ui.admin_tickets import AdminTicketsScreen
from ui.admin_users import AdminUsersScreen
from ui.view_issues import ViewIssuesScreen


class MainApp(ctk.CTk):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.current_user = None

        self.title("Ticketing System")
        self.geometry("800x600")

        # Initialize instance attributes
        self.login_screen = None
        self.register_screen = None
        self.user_screen = None
        self.tech_screen = None
        self.admin_tickets_screen = None
        self.admin_users_screen = None
        self.view_issues_screen = None
        self.navbar = None
        self.tickets_button = None
        self.users_button = None
        self.view_issues_button = None

        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        self.login_screen = LoginScreen(self, self)
        self.login_screen.pack(fill="both", expand=True)

    def create_register_screen(self):
        self.clear_screen()
        self.register_screen = RegisterScreen(self, self)
        self.register_screen.pack(fill="both", expand=True)

    def create_main_screen(self):
        self.clear_screen()
        if self.current_user[3] == 'user':
            self.user_screen = UserScreen(self, self)
            self.user_screen.pack(fill="both", expand=True)
            self.view_issues_button = ctk.CTkButton(self, text="View Issues", command=self.create_view_issues_screen)
            self.view_issues_button.pack(pady=10)
        elif self.current_user[3] == 'tech':
            self.tech_screen = TechScreen(self, self)
            self.tech_screen.pack(fill="both", expand=True)
            self.view_issues_button = ctk.CTkButton(self, text="View Issues", command=self.create_view_issues_screen)
            self.view_issues_button.pack(pady=10)
        elif self.current_user[3] == 'admin':
            self.create_admin_navbar()
            self.create_admin_tickets_screen()

    def create_admin_navbar(self):
        self.navbar = ctk.CTkFrame(self)
        self.navbar.pack(side="top", fill="x")

        self.tickets_button = ctk.CTkButton(self.navbar, text="Tickets", command=self.create_admin_tickets_screen)
        self.tickets_button.pack(side="left", padx=10, pady=10)

        self.users_button = ctk.CTkButton(self.navbar, text="Users", command=self.create_admin_users_screen)
        self.users_button.pack(side="left", padx=10, pady=10)

    def create_admin_tickets_screen(self):
        self.clear_screen(exclude_navbar=True)
        self.admin_tickets_screen = AdminTicketsScreen(self, self)
        self.admin_tickets_screen.pack(fill="both", expand=True)

    def create_admin_users_screen(self):
        self.clear_screen(exclude_navbar=True)
        self.admin_users_screen = AdminUsersScreen(self, self)
        self.admin_users_screen.pack(fill="both", expand=True)

    def create_view_issues_screen(self):
        self.clear_screen()
        self.view_issues_screen = ViewIssuesScreen(self, self)
        self.view_issues_screen.pack(fill="both", expand=True)

    def clear_screen(self, exclude_navbar=False):
        for widget in self.winfo_children():
            if exclude_navbar and widget == self.navbar:
                continue
            widget.destroy()


if __name__ == "__main__":
    import sqlite3
    from database import setup_database

    conn = sqlite3.connect('ticketing_system.db')
    setup_database(conn)

    app = MainApp(conn)
    app.mainloop()
