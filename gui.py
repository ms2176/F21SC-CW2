import tkinter as tk
from tkinter import messagebox, filedialog
import os

from task2 import run_task_2a, run_task_2b
from task3 import run_task_3a, run_task_3b
from task4 import run_task_4

FILE_PATH = "issuu_cw2.json"

def choose_file():
    global FILE_PATH
    path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if path:
        FILE_PATH = path
        messagebox.showinfo("File Loaded", f"Using data file:\n{FILE_PATH}")

def run_task(action):
    doc = doc_entry.get().strip()
    user = user_entry.get().strip()

    if not os.path.exists(FILE_PATH):
        messagebox.showerror("Error", f"Data file not found:\n{FILE_PATH}")
        return

    try:
        if action == "2A":
            run_task_2a(FILE_PATH, doc)
        elif action == "2B":
            run_task_2b(FILE_PATH, doc)
        elif action == "3A":
            run_task_3a(FILE_PATH, doc)
        elif action == "3B":
            run_task_3b(FILE_PATH, doc)
        elif action == "4":
            run_task_4(FILE_PATH, doc)
        else:
            messagebox.showerror("Error", "Unknown task")
            return

    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("CW2 Analytics")

tk.Button(root, text="Load File", command=choose_file).grid(row=0, column=0, padx=5, pady=5)

tk.Label(root, text="Document ID:").grid(row=0, column=1, sticky="w")
doc_entry = tk.Entry(root, width=30)
doc_entry.grid(row=0, column=2, padx=5)

tk.Label(root, text="User ID:").grid(row=0, column=3, sticky="w")
user_entry = tk.Entry(root, width=20)
user_entry.grid(row=0, column=4, padx=5)

# --- Button frame ---
btn_frame = tk.Frame(root)
btn_frame.grid(row=1, column=0, columnspan=5, pady=10)

tasks = ["2A", "2B", "3A", "3B", "4", "5", "6"]
for t in tasks:
    tk.Button(btn_frame, text=t, width=6, command=lambda task=t: run_task(task)).pack(side="left", padx=5)

root.mainloop()
