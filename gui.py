# gui.py
import tkinter as tk
from tkinter import messagebox
from task2 import run_task_2a, run_task_2b
from task3 import run_task_3a, run_task_3b
from task4 import run_task_4

FILE_PATH = "issuu_cw2.json"

def run_task(action):
    doc = doc_entry.get().strip()

    if not doc:
        messagebox.showerror("Missing Input", "Enter a document UUID.")
        return

    if action == "2A":
        result = run_task_2a(FILE_PATH, doc)
    elif action == "2B":
        result = run_task_2b(FILE_PATH, doc)
    elif action == "3A":
        result = run_task_3a(FILE_PATH, doc)
    elif action == "3B":
        result = run_task_3b(FILE_PATH, doc)
    elif action == "4":
        result = run_task_4(FILE_PATH, doc)
    else:
        messagebox.showerror("Invalid Action", "Unknown action requested.")
        return

    if result is None:
        messagebox.showinfo("No Data", "No records found for this document.")


root = tk.Tk()
root.title("CW2 - Task 2 Analysis")

frm = tk.Frame(root, padx=10, pady=10)
frm.pack()

tk.Label(frm, text="Document UUID:").grid(row=0, column=0, sticky="w")
doc_entry = tk.Entry(frm, width=50)
doc_entry.grid(row=0, column=1)

btn_2a = tk.Button(frm, text="Task 2A", width=20, command=lambda: run_task("2A"))
btn_2a.grid(row=1, column=0, pady=10)

btn_2b = tk.Button(frm, text="Task 2B", width=20, command=lambda: run_task("2B"))
btn_2b.grid(row=1, column=1, pady=10)

btn_3a = tk.Button(frm, text="Task 3A", width=20, command=lambda: run_task("3A"))
btn_3a.grid(row=2, column=0, pady=10)

btn_3b = tk.Button(frm, text="Task 3B", width=20, command=lambda: run_task("3B"))
btn_3b.grid(row=2, column=1, pady=10)

btn_4 = tk.Button(frm, text="Task 4", width=20, command=lambda: run_task("4"))
btn_4.grid(row=3, column=0, pady=10)

root.mainloop()
