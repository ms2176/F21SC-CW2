import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
from PIL import Image, ImageTk, ImageOps
from task2 import run_task_2a, run_task_2b
from task3 import run_task_3a, run_task_3b
from task4 import run_task_4
from task5 import run_task_5d
from task6 import run_task_6

DEFAULT_DATA_FILE = "issuu_cw2.json"


class AnalyticsGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("F21SC CW2 Analytics")

        self.data_file = DEFAULT_DATA_FILE

        # --- Top controls: file + IDs ---
        top_frame = tk.Frame(root, padx=10, pady=10)
        top_frame.pack(fill=tk.X)

        load_btn = tk.Button(top_frame, text="Load file", command=self.choose_file, width=10)
        load_btn.grid(row=0, column=0, padx=5)

        tk.Label(top_frame, text="Enter document ID:").grid(row=0, column=1, sticky="w")
        self.doc_entry = tk.Entry(top_frame, width=40)
        self.doc_entry.grid(row=0, column=2, padx=5)

        tk.Label(top_frame, text="Enter user ID:").grid(row=0, column=3, sticky="w")
        self.user_entry = tk.Entry(top_frame, width=30)
        self.user_entry.grid(row=0, column=4, padx=5)

        # --- Task selection buttons ---
        task_frame = tk.Frame(root, padx=10, pady=5)
        task_frame.pack(fill=tk.X)

        tk.Label(task_frame, text="Task Selection").grid(row=0, column=0, sticky="w", pady=(0, 5))

        # Tasks mapping to functions
        self.task_map = {
            "2A": run_task_2a,
            "2B": run_task_2b,
            "3A": run_task_3a,
            "3B": run_task_3b,
            "4": run_task_4,
            "5D": run_task_5d,
            "6": run_task_6
        }

        for idx, task_name in enumerate(self.task_map.keys()):
            tk.Button(
                task_frame,
                text=task_name,
                width=6,
                command=lambda t=task_name: self.run_task(t)
            ).grid(row=1, column=idx, padx=5)

        # --- Output area ---
        output_frame = tk.Frame(root, padx=10, pady=10)
        output_frame.pack(fill=tk.BOTH, expand=True)

        self.output = scrolledtext.ScrolledText(
            output_frame, wrap=tk.WORD, height=10, width=100
        )
        self.output.pack(fill=tk.BOTH, expand=True)
        # Image display area (for Task 6 graph)
        self.image_label = tk.Label(output_frame)
        self.image_label.pack(pady=10)
        self.write_output("Select a task to display results here.\n")

    # ---- helpers ---------------------------------------------------------

    def write_output(self, text: str) -> None:
        self.output.configure(state=tk.NORMAL)
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)
        self.output.configure(state=tk.DISABLED)
        self.image_label.configure(image='')

    def append_output(self, text: str) -> None:
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, text)
        self.output.configure(state=tk.DISABLED)

    def choose_file(self) -> None:
        path = filedialog.askopenfilename(
            title="Select data file",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if path:
            self.data_file = path
            messagebox.showinfo("File loaded", f"Using data file:\n{path}")

    def require_document_id(self) -> str:
        doc = self.doc_entry.get().strip()
        if not doc:
            messagebox.showwarning("Missing document ID", "Please enter a document ID.")
            raise ValueError("missing document id")
        return doc

    def require_user_id(self) -> str:
        user = self.user_entry.get().strip()
        if not user:
            messagebox.showwarning("Missing user ID", "Please enter a user ID for this task.")
            raise ValueError("missing user id")
        return user
    
    def require_data_file(self) -> str:
        if not os.path.exists(self.data_file):
            messagebox.showerror(
                "Data file not found",
                f"Data file does not exist:\n{self.data_file}",
            )
            raise FileNotFoundError(self.data_file)
        return self.data_file

    # ---- Task runner -----------------------------------------------------

    def run_task(self, task_name: str) -> None:
        """
        Validate required inputs for each task, run the task function and display output.
        Tasks 2A,2B,3A,3B,4,5D require document id.
        Task 6 requires document id AND user id.
        """
        try:
            data_file = self.require_data_file()
            func = self.task_map.get(task_name)

            if not func:
                messagebox.showerror("Error", f"Task {task_name} not implemented.")
                return

            # Validate inputs based on task
            if task_name in ["2A", "2B", "3A", "3B", "4", "5D"]:
                try:
                    doc_id = self.require_document_id()
                except ValueError:
                    # require_document_id already showed a warning
                    return
                # Call function with (file, doc)
                result = func(data_file, doc_id)

            elif task_name == "6":
                # Task 6 needs both document and user
                try:
                    doc_id = self.require_document_id()
                    user_id = self.require_user_id()
                except ValueError:
                    return
                # Call function with (file, doc, user)
                result = func(data_file, doc_id, user_id)

            # Handle Task 6 image output (PNG path returned)
            if task_name == "6":
                if isinstance(result, str) and result.endswith(".png") and os.path.exists(result):
                    try:
                        img = Image.open(result)
                        max_width, max_height = 700, 350  # adjust to taste
                        img = ImageOps.contain(img, (max_width, max_height), Image.Resampling.LANCZOS)
                        self.photo = ImageTk.PhotoImage(img)
                        self.write_output(f"Generated Also-Likes Graph:\n{result}\n")
                        self.image_label.configure(image=self.photo)
                    except Exception as img_err:
                        self.write_output("Failed to load image into GUI.\n")
                        messagebox.showerror("Image error", str(img_err))

            # Non-image tasks: display returned result (string/list/etc.)
            if result is not None:
                self.write_output(str(result))
            else:
                self.write_output(f"Task {task_name} completed.\n")

        except FileNotFoundError:
            # require_data_file already raised and showed an error
            return
        except Exception as e:
            # Generic catch — show in a popup so user notices
            messagebox.showerror("Error", str(e))



if __name__ == "__main__":
    root = tk.Tk()
    app = AnalyticsGUI(root)
    root.mainloop()
