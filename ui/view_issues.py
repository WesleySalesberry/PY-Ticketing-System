import customtkinter as ctk
import tkinter as tk
from tkinter import simpledialog, messagebox


class ViewIssuesScreen(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        self.back_button = ctk.CTkButton(self, text="Back", command=self.app.create_main_screen)
        self.back_button.pack(pady=10)

        self.issue_listbox = tk.Listbox(self)
        self.issue_listbox.pack(pady=10, fill="both", expand=True)

        self.refresh_button = ctk.CTkButton(self, text="Refresh Issues", command=self.load_issues)
        self.refresh_button.pack(pady=10)

        self.view_notes_button = ctk.CTkButton(self, text="View Notes", command=self.view_notes)
        self.view_notes_button.pack(pady=10)

        self.add_note_button = ctk.CTkButton(self, text="Add Note", command=self.add_note)
        self.add_note_button.pack(pady=10)

        self.load_issues()

    def load_issues(self):
        self.issue_listbox.delete(0, tk.END)
        c = self.app.conn.cursor()

        if self.app.current_user[3] == 'user':
            c.execute('SELECT * FROM issues WHERE user_id = ?', (self.app.current_user[0],))
        else:
            c.execute('SELECT * FROM issues')

        issues = c.fetchall()
        for issue in issues:
            tech = self.get_tech_name(issue[5])
            self.issue_listbox.insert(tk.END,
                                      f"{issue[0]}: {issue[2]} - {issue[3]} (Severity: {issue[4]}) (Tech: {tech})")

    def get_tech_name(self, tech_id):
        if tech_id:
            c = self.app.conn.cursor()
            c.execute('SELECT username FROM users WHERE id = ?', (tech_id,))
            tech = c.fetchone()
            return tech[0] if tech else "Unknown"
        return "None"

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

    def add_note(self):
        if self.app.current_user[3] == 'user':
            messagebox.showerror("Error", "Users cannot add notes")
            return

        selected_issue = self.issue_listbox.get(tk.ACTIVE)
        if not selected_issue:
            messagebox.showerror("Error", "No issue selected")
            return
        issue_id = int(selected_issue.split(':')[0])

        if self.app.current_user[3] == 'tech':
            c = self.app.conn.cursor()
            c.execute('SELECT tech_id FROM issues WHERE id = ?', (issue_id,))
            current_tech = c.fetchone()
            if current_tech and current_tech[0] != self.app.current_user[0]:
                messagebox.showerror("Error", "Only the tech who checked out the issue can add notes")
                return

        note = simpledialog.askstring("Note", "Enter note:")
        if note:
            c = self.app.conn.cursor()
            c.execute('INSERT INTO notes (issue_id, tech_id, note) VALUES (?, ?, ?)',
                      (issue_id, self.app.current_user[0], note))
            self.app.conn.commit()
            messagebox.showinfo("Success", "Note added successfully")
        else:
            messagebox.showinfo("Info", "Note addition cancelled")
