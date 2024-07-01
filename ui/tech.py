import customtkinter as ctk
import tkinter as tk
from tkinter import simpledialog, messagebox


class TechScreen(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        self.button_frame = ctk.CTkFrame(self)
        self.issue_frame = ctk.CTkFrame(self)

        # self.back_button = ctk.CTkButton(self.button_frame, text="Back", command=self.app.create_main_screen)
        self.refresh_button = ctk.CTkButton(self.button_frame, text="Refresh Issues", command=self.load_issues)
        self.filter_var = tk.StringVar(value="All")
        self.filter_menu = ctk.CTkOptionMenu(self.button_frame, variable=self.filter_var,
                                             values=["All", "Low", "Medium", "High"], command=self.load_issues)
        self.checkout_button = ctk.CTkButton(self.button_frame, text="Check Out Issue", command=self.checkout_issue)
        self.view_notes_button = ctk.CTkButton(self.button_frame, text="View Notes", command=self.view_notes)
        self.severity_label = ctk.CTkLabel(self.button_frame, text="Severity")
        self.severity_var = tk.StringVar(value="Low")
        self.severity_menu = ctk.CTkOptionMenu(self.button_frame, variable=self.severity_var,
                                               values=["Low", "Medium", "High"])
        self.classify_button = ctk.CTkButton(self.button_frame, text="Classify Severity",
                                             command=self.classify_severity)
        self.leave_note_button = ctk.CTkButton(self.button_frame, text="Leave Note", command=self.leave_note)
        self.issue_listbox = tk.Listbox(self.issue_frame)

        self.setup_layout()
        self.load_issues()

    def setup_layout(self):
        self.button_frame.pack(side="left", fill="y", padx=10, pady=10)
        self.issue_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # self.back_button.pack(pady=5)
        self.refresh_button.pack(pady=5)
        self.filter_menu.pack(pady=5)
        self.checkout_button.pack(pady=5)
        self.view_notes_button.pack(pady=5)
        self.severity_label.pack(pady=5)
        self.severity_menu.pack(pady=5)
        self.classify_button.pack(pady=5)
        self.leave_note_button.pack(pady=5)

        self.issue_listbox.pack(pady=5, fill="both", expand=True)

    def load_issues(self, _=None):
        self.issue_listbox.delete(0, tk.END)
        c = self.app.conn.cursor()
        severity_filter = self.filter_var.get()
        if severity_filter == "All":
            c.execute('SELECT * FROM issues')
        else:
            c.execute('SELECT * FROM issues WHERE severity = ?', (severity_filter,))
        issues = c.fetchall()
        for issue in issues:
            self.issue_listbox.insert(tk.END, f"{issue[0]}: {issue[2]} - {issue[3]} (Severity: {issue[4]})")

    def checkout_issue(self):
        selected_issue = self.issue_listbox.get(tk.ACTIVE)
        if not selected_issue:
            messagebox.showerror("Error", "No issue selected")
            return
        issue_id = int(selected_issue.split(':')[0])
        c = self.app.conn.cursor()
        c.execute('SELECT tech_id FROM issues WHERE id = ?', (issue_id,))
        current_tech = c.fetchone()
        if current_tech and current_tech[0] is not None:
            messagebox.showerror("Error", "This issue is already checked out by another tech")
            return
        c.execute('UPDATE issues SET tech_id = ? WHERE id = ?', (self.app.current_user[0], issue_id))
        self.app.conn.commit()
        messagebox.showinfo("Success", "Issue checked out successfully")

    def classify_severity(self):
        selected_issue = self.issue_listbox.get(tk.ACTIVE)
        if not selected_issue:
            messagebox.showerror("Error", "No issue selected")
            return
        issue_id = int(selected_issue.split(':')[0])
        severity = self.severity_var.get()
        c = self.app.conn.cursor()
        c.execute('SELECT tech_id FROM issues WHERE id = ?', (issue_id,))
        current_tech = c.fetchone()
        if current_tech and current_tech[0] != self.app.current_user[0]:
            messagebox.showerror("Error", "This issue is checked out by another tech")
            return
        if severity:
            c.execute('UPDATE issues SET severity = ? WHERE id = ?', (severity, issue_id))
            self.app.conn.commit()
            self.load_issues()
        else:
            messagebox.showinfo("Info", "Severity update cancelled")

    def leave_note(self):
        selected_issue = self.issue_listbox.get(tk.ACTIVE)
        if not selected_issue:
            messagebox.showerror("Error", "No issue selected")
            return
        issue_id = int(selected_issue.split(':')[0])
        c = self.app.conn.cursor()
        c.execute('SELECT tech_id FROM issues WHERE id = ?', (issue_id,))
        current_tech = c.fetchone()
        if current_tech and current_tech[0] != self.app.current_user[0]:
            messagebox.showerror("Error", "This issue is checked out by another tech")
            return
        note = simpledialog.askstring("Note", "Enter note:")
        if note:
            c.execute('INSERT INTO notes (issue_id, tech_id, note) VALUES (?, ?, ?)',
                      (issue_id, self.app.current_user[0], note))
            self.app.conn.commit()
            messagebox.showinfo("Success", "Note added successfully")
        else:
            messagebox.showinfo("Info", "Note addition cancelled")

    def view_notes(self):
        selected_issue = self.issue_listbox.get(tk.ACTIVE)
        if not selected_issue:
            messagebox.showerror("Error", "No issue selected")
            return
        issue_id = int(selected_issue.split(':')[0])
        c = self.app.conn.cursor()
        c.execute('SELECT note FROM notes WHERE issue_id = ?', (issue_id,))
        notes = c.fetchall()
        if notes:
            notes_text = "\n".join(note[0] for note in notes)
            messagebox.showinfo("Notes", notes_text)
        else:
            messagebox.showinfo("Notes", "No notes for this issue")
