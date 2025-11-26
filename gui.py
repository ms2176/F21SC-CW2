# gui.py
import tkinter as tk
from tkinter import messagebox
from task2 import (
    get_country_counts_2a,
    get_continent_counts_2b
)
from continent import continent_lookup
from histogram import plot_histogram

FILE_PATH = "issuu_cw2.json"

def run_task(action):
    doc = doc_entry.get().strip()

    if not doc:
        messagebox.showerror("Missing Input", "Enter a document UUID.")
        return

    country_counter = get_country_counts_2a(FILE_PATH, doc)

    if not country_counter:
        messagebox.showinfo("No Data", "No records found for this document.")
        return

    if action == "2A":
        plot_histogram(
            counter=country_counter,
            title=f"Viewer distribution by country for {doc}",
            xlabel="Country"
        )

    elif action == "2B":
        continent_counter = get_continent_counts_2b(country_counter, continent_lookup)

        plot_histogram(
            counter=continent_counter,
            title=f"Viewer distribution by continent for {doc}",
            xlabel="Continent"
        )


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

root.mainloop()
