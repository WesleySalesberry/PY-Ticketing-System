import customtkinter as ctk
import tkinter as tk


class AdminTicketsScreen(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        # Initialize instance attributes
        self.button_frame = None
        self.issue_frame = None
        self.refresh_button = None
        self.sort_by_user_button = None
        self.sort_by_severity_button = None
        self.issue_listbox = None

        self.setup_layout()

    def setup_layout(self):
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.issue_frame = ctk.CTkFrame(self)
        self.issue_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.refresh_button = ctk.CTkButton(self.button_frame, text="Refresh Issues", command=self.load_issues)
        self.refresh_button.pack(pady=10)

        self.sort_by_user_button = ctk.CTkButton(self.button_frame, text="Sort by User",
                                                 command=lambda: self.load_issues(sort_by="user"))
        self.sort_by_user_button.pack(pady=10)

        self.sort_by_severity_button = ctk.CTkButton(self.button_frame, text="Sort by Severity",
                                                     command=lambda: self.load_issues(sort_by="severity"))
        self.sort_by_severity_button.pack(pady=10)

        self.issue_listbox = tk.Listbox(self.issue_frame)
        self.issue_listbox.pack(pady=10, fill="both", expand=True)

        self.load_issues()

    def load_issues(self, sort_by=None):
        self.issue_listbox.delete(0, tk.END)
        c = self.app.conn.cursor()

        if sort_by == "user":
            c.execute('''
                SELECT issues.id, issues.title, issues.description, issues.severity, users.username
                FROM issues
                LEFT JOIN users ON issues.tech_id = users.id
                ORDER BY issues.user_id
            ''')
        elif sort_by == "severity":
            c.execute('''
                SELECT issues.id, issues.title, issues.description, issues.severity, users.username
                FROM issues
                LEFT JOIN users ON issues.tech_id = users.id
                ORDER BY issues.severity
            ''')
        else:
            c.execute('''
                SELECT issues.id, issues.title, issues.description, issues.severity, users.username
                FROM issues
                LEFT JOIN users ON issues.tech_id = users.id
            ''')

        issues = c.fetchall()
        for issue in issues:
            tech = issue[4] if issue[4] else "None"
            self.issue_listbox.insert(tk.END,
                                      f"{issue[0]}: {issue[1]} - {issue[2]} (Severity: {issue[3]}, Tech: {tech})")
