import customtkinter as ctk
from tkinter import messagebox


class UserScreen(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        self.issue_title_label = ctk.CTkLabel(self, text="Issue Title")
        self.issue_title_label.pack(pady=10)

        self.issue_title_entry = ctk.CTkEntry(self)
        self.issue_title_entry.pack(pady=10)

        self.issue_description_label = ctk.CTkLabel(self, text="Issue Description")
        self.issue_description_label.pack(pady=10)

        self.issue_description_entry = ctk.CTkEntry(self)
        self.issue_description_entry.pack(pady=10)

        self.submit_issue_button = ctk.CTkButton(self, text="Submit Issue", command=self.submit_issue)
        self.submit_issue_button.pack(pady=10)

    def submit_issue(self):
        title = self.issue_title_entry.get()
        description = self.issue_description_entry.get()

        c = self.app.conn.cursor()
        c.execute('INSERT INTO issues (user_id, title, description) VALUES (?, ?, ?)',
                  (self.app.current_user[0], title, description))
        self.app.conn.commit()

        messagebox.showinfo("Success", "Issue submitted successfully")
