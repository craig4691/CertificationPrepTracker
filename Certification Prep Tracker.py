"""
Author: Craig Moy
Date: 5/1/25
Program: Certification Prep Tracker
Description: A GUI app to track IT certification study progress.
"""

import tkinter as tk
from tkinter import messagebox, filedialog, Toplevel, PhotoImage

class CertPrepTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Certification Prep Tracker")
        self.study_data = []  # List to store topic dictionaries

        # Load and display two relevant images with alt-text-style labels
        self.logo_image = PhotoImage(file="checklist_icon.png").subsample(3, 3)  # Checklist icon
        self.logo_label = tk.Label(root, image=self.logo_image)
        self.logo_label.pack()
        tk.Label(root, text="Alt Text: Checklist icon representing task tracking").pack()

        self.motivation_image = PhotoImage(file="network_server_icon.png").subsample(3, 3)  # Network server icon
        self.motivation_label = tk.Label(root, image=self.motivation_image)
        self.motivation_label.pack()
        tk.Label(root, text="Alt Text: Network server icon representing IT certifications").pack()

        self.create_main_widgets()

    def create_main_widgets(self):
        # Label and entry for main topic
        tk.Label(self.root, text="Certification Topic:").pack()
        self.topic_entry = tk.Entry(self.root, width=40)
        self.topic_entry.pack()

        # Label and entry for subtask
        tk.Label(self.root, text="Optional Subtask:").pack()
        self.subtask_entry = tk.Entry(self.root, width=40)
        self.subtask_entry.pack()

        # Label and entry for progress percent
        tk.Label(self.root, text="Progress (%):").pack()
        self.progress_entry = tk.Entry(self.root, width=10)
        self.progress_entry.pack()

        # Buttons for adding and managing data
        tk.Button(self.root, text="Add Topic", command=self.add_topic).pack()
        tk.Button(self.root, text="Toggle Finished", command=self.toggle_finished).pack()
        tk.Button(self.root, text="Save Progress", command=self.save_progress).pack()
        tk.Button(self.root, text="Clear All", command=self.clear_all).pack()
        tk.Button(self.root, text="View Summary", command=self.open_summary_window).pack()
        tk.Button(self.root, text="Exit", command=self.root.quit).pack()

        # Listbox for topic display
        self.topic_listbox = tk.Listbox(self.root, width=70)
        self.topic_listbox.pack()

    def add_topic(self):
        """Adds a topic and optional subtask to the list with input validation."""
        topic = self.topic_entry.get().strip()
        subtask = self.subtask_entry.get().strip()
        progress_str = self.progress_entry.get().strip()

        if not topic or not progress_str:
            messagebox.showwarning("Missing Info", "Please enter both topic and progress.")
            return

        try:
            progress = float(progress_str)
            if not 0 <= progress <= 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Progress must be a number between 0 and 100.")
            return

        # Build label with or without subtask
        label = f"{topic} > {subtask}" if subtask else topic
        display = f"[ ] {label} - {progress}%"

        self.topic_listbox.insert(tk.END, display)
        self.study_data.append({'topic': label, 'progress': progress, 'finished': False})

        # Clear entry boxes
        self.topic_entry.delete(0, tk.END)
        self.subtask_entry.delete(0, tk.END)
        self.progress_entry.delete(0, tk.END)

    def toggle_finished(self):
        """Marks selected topic as finished/unfinished and updates the display."""
        selection = self.topic_listbox.curselection()
        if not selection:
            messagebox.showinfo("No Selection", "Select a topic first.")
            return

        idx = selection[0]
        entry = self.study_data[idx]
        entry['finished'] = not entry['finished']

        status = "[✓]" if entry['finished'] else "[ ]"
        updated_display = f"{status} {entry['topic']} - {entry['progress']}%"
        self.topic_listbox.delete(idx)
        self.topic_listbox.insert(idx, updated_display)

    def save_progress(self):
        """Saves current progress to a text or CSV file."""
        if not self.study_data:
            messagebox.showinfo("No Data", "Nothing to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"),
                                                            ("CSV Files", "*.csv"),
                                                            ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                for entry in self.study_data:
                    status = "Finished" if entry['finished'] else "Unfinished"
                    file.write(f"{entry['topic']},{entry['progress']}%,{status}\n")
            messagebox.showinfo("Saved", "Progress saved successfully!")

    def clear_all(self):
        """Clears all entries from the list and memory."""
        self.topic_listbox.delete(0, tk.END)
        self.study_data.clear()

    def open_summary_window(self):
        """Opens a second window showing summary of total, finished, and average progress."""
        summary_win = Toplevel(self.root)
        summary_win.title("Summary")

        total = len(self.study_data)
        finished = sum(1 for x in self.study_data if x['finished'])
        avg_progress = sum(x['progress'] for x in self.study_data) / total if total else 0

        tk.Label(summary_win, text=f"Total Topics: {total}").pack()
        tk.Label(summary_win, text=f"Finished: {finished}").pack()
        tk.Label(summary_win, text=f"Average Progress: {avg_progress:.2f}%").pack()
        tk.Button(summary_win, text="Close", command=summary_win.destroy).pack()


# Run the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    app = CertPrepTracker(root)
    root.mainloop()

