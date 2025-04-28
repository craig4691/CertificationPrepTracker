# Certification Prep Tracker
# Author: Craig Moy
# Date: 4/28/2025
# Description: A simple Tkinter GUI to track study topics for certifications

import tkinter as tk
from tkinter import messagebox

class CertificationPrepTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Certification Prep Tracker")

        # Create list to hold study topics
        self.topics = []

        # Entry for new topic
        self.topic_entry = tk.Entry(root, width=40)
        self.topic_entry.pack(pady=10)

        # Add topic button
        self.add_button = tk.Button(root, text="Add Topic", command=self.add_topic)
        self.add_button.pack(pady=5)

        # Listbox to display topics
        self.topic_listbox = tk.Listbox(root, width=50, height=10)
        self.topic_listbox.pack(pady=10)

        # Mark as completed button
        self.complete_button = tk.Button(root, text="Mark as Completed", command=self.mark_completed)
        self.complete_button.pack(pady=5)

        # Label to show progress
        self.progress_label = tk.Label(root, text="Progress: 0%")
        self.progress_label.pack(pady=10)

    def add_topic(self):
        topic = self.topic_entry.get()
        if topic:
            self.topics.append({"name": topic, "completed": False})
            self.update_listbox()
            self.topic_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a study topic.")

    def mark_completed(self):
        selected = self.topic_listbox.curselection()
        if selected:
            index = selected[0]
            self.topics[index]["completed"] = True
            self.update_listbox()
            self.update_progress()
        else:
            messagebox.showwarning("Selection Error", "Please select a topic to mark as completed.")

    def update_listbox(self):
        self.topic_listbox.delete(0, tk.END)
        for topic in self.topics:
            status = "[✓]" if topic["completed"] else "[ ]"
            self.topic_listbox.insert(tk.END, f"{status} {topic['name']}")
        self.update_progress()

    def update_progress(self):
        if not self.topics:
            progress = 0
        else:
            completed = sum(1 for t in self.topics if t["completed"])
            progress = int((completed / len(self.topics)) * 100)
        self.progress_label.config(text=f"Progress: {progress}%")

if __name__ == "__main__":
    root = tk.Tk()
    app = CertificationPrepTracker(root)
    root.mainloop()
