import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os
import re
from collections import Counter, defaultdict

from load import load_data
from continent import continent_lookup
from task5 import also_likes, sort_by_shared_readers
from task6 import generate_dot_graph
from task2ver1 import get_country_counts, plot_histogram

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

        btn_specs = [
            ("2a", self.run_task_2a),
            ("2b", self.run_task_2b),
            ("3a", self.run_task_3a),
            ("3b", self.run_task_3b),
            ("4", self.run_task_4),
            ("5d", self.run_task_5d),
            ("6", self.run_task_6),
        ]

        for idx, (label, handler) in enumerate(btn_specs, start=0):
            tk.Button(task_frame, text=label, width=6, command=handler).grid(
                row=1, column=idx, padx=5
            )

        # --- Output area ---
        output_frame = tk.Frame(root, padx=10, pady=10)
        output_frame.pack(fill=tk.BOTH, expand=True)

        self.output = scrolledtext.ScrolledText(
            output_frame, wrap=tk.WORD, height=20, width=100
        )
        self.output.pack(fill=tk.BOTH, expand=True)
        self.write_output("Select a task to display results here.\n")

    # ---- helpers ---------------------------------------------------------

    def write_output(self, text: str) -> None:
        self.output.configure(state=tk.NORMAL)
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)
        self.output.configure(state=tk.DISABLED)

    def append_output(self, text: str) -> None:
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, text)
        self.output.configure(state=tk.DISABLED)

    def choose_file(self) -> None:
        path = filedialog.askopenfilename(
            title="Select data file",
            filetypes=[("JSON lines", "*.json"), ("All files", "*.*")],
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

    def require_data_file(self) -> str:
        if not os.path.exists(self.data_file):
            messagebox.showerror(
                "Data file not found",
                f"Data file does not exist:\n{self.data_file}",
            )
            raise FileNotFoundError(self.data_file)
        return self.data_file

    # ---- task implementations -------------------------------------------

    # Task 2a: histogram by country
    def run_task_2a(self) -> None:
        try:
            file_path = self.require_data_file()
            doc_id = self.require_document_id()
            country_counts = get_country_counts(file_path, doc_id)
            if not country_counts:
                self.write_output(f"No records found for document:\n{doc_id}")
                return

            self.write_output(
                f"Task 2a Viewer distribution by country for document:\n{doc_id}\n"
                "A bar chart window will open.\n"
            )
            plot_histogram(
                counter=country_counts,
                title=f"Viewer distribution by country for {doc_id}",
                xlabel="Country",
            )
        except Exception as exc:
            self.write_output(f"Error in task 2a:\n{exc}")

    # Task 2b: histogram by continent
    def run_task_2b(self) -> None:
        try:
            file_path = self.require_data_file()
            doc_id = self.require_document_id()

            from task2ver1 import get_country_counts, get_continent_counts, plot_histogram

            country_counts = get_country_counts(file_path, doc_id)
            if not country_counts:
                self.write_output(f"No records found for document:\n{doc_id}")
                return

            continent_counts = get_continent_counts(country_counts, continent_lookup)

            self.write_output(
                f"Task 2b Viewer distribution by continent for document:\n{doc_id}\n"
                "A bar chart window will open.\n"
            )
            plot_histogram(
                counter=continent_counts,
                title=f"Viewer distribution by continent for {doc_id}",
                xlabel="Continent",
            )
        except Exception as exc:
            self.write_output(f"Error in task 2b:\n{exc}")

    # Task 3a: histogram of user agents
    def run_task_3a(self) -> None:
        try:
            import matplotlib.pyplot as plt

            file_path = self.require_data_file()

            useragents = Counter(
                record.get("visitor_useragent")
                for record in load_data(file_path)
                if record.get("visitor_useragent")
            )

            if not useragents:
                self.write_output("No user agent data found.")
                return

            self.write_output("Task 3a – Viewer distribution by user agent.\n")

            plt.figure(figsize=(10, 5))
            plt.bar(useragents.keys(), useragents.values())
            plt.xlabel("User Agent")
            plt.ylabel("Viewer count")
            plt.title("Viewer distribution by user agent")
            plt.xticks(rotation=0)
            plt.tight_layout()
            plt.show()
        except Exception as exc:
            self.write_output(f"Error in task 3a:\n{exc}")

    # Task 3b: histogram by main browser
    def run_task_3b(self) -> None:
        try:
            import matplotlib.pyplot as plt

            file_path = self.require_data_file()

            def get_main_browser(useragent: str) -> str:
                if not useragent:
                    return "Unknown"
                match = re.match(r"([^\\s/]+)", useragent)
                return match.group(1) if match else "Unknown"

            main_browsers = Counter(
                get_main_browser(record.get("visitor_useragent"))
                for record in load_data(file_path)
            )

            if not main_browsers:
                self.write_output("No browser data found.")
                return

            self.write_output("Task 3b – Viewer distribution by main browser.\n")

            plt.figure(figsize=(10, 5))
            plt.bar(main_browsers.keys(), main_browsers.values())
            plt.xlabel("Browser")
            plt.ylabel("Viewer count")
            plt.title("Viewer distribution by main browser")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        except Exception as exc:
            self.write_output(f"Error in task 3b:\n{exc}")

    # Task 4: top 10 readers by total reading time (text)
    def run_task_4(self) -> None:
        try:
            file_path = self.require_data_file()

            user_readtime: defaultdict[str, int] = defaultdict(int)
            for record in load_data(file_path):
                user = record.get("visitor_uuid")
                readtime = record.get("event_readtime")
                if user and isinstance(readtime, (int, float)):
                    user_readtime[user] += readtime

            top_readers = sorted(
                user_readtime.items(), key=lambda x: x[1], reverse=True
            )[:10]

            if not top_readers:
                self.write_output("No reader time data found.")
                return

            lines = ["Task 4  Top 10 readers by total reading time:\n"]
            lines.append(f"{'Visitor UUID':<24} {'Total Read Time':>15}")
            lines.append("-" * 42)
            for visitor, total in top_readers:
                lines.append(f"{visitor:<24} {total:>15}")

            self.write_output("\n".join(lines))
        except Exception as exc:
            self.write_output(f"Error in task 4:\n{exc}")

    # Task 5d: also-likes list (top 10 documents) as text
    def run_task_5d(self) -> None:
        try:
            file_path = self.require_data_file()
            doc_id = self.require_document_id()

            docs = also_likes(doc_id, file_path, sort_by_shared_readers)
            if isinstance(docs, str):
                self.write_output(docs)
                return

            lines = [f"Task 5d  Top 10 'also like' documents for:\n{doc_id}\n"]
            for idx, d in enumerate(docs, start=1):
                lines.append(f"{idx:2d}. {d}  (…{d[-4:]})")

            self.write_output("\n".join(lines))
        except Exception as exc:
            self.write_output(f"Error in task 5d:\n{exc}")

    # Task 6: also-likes graph using DOT / Graphviz
    def run_task_6(self) -> None:
        try:
            file_path = self.require_data_file()
            doc_id = self.require_document_id()
            visitor_id = self.user_entry.get().strip() or None

            # Generate DOT graph
            generate_dot_graph(doc_id, visitor_id, file_path, sort_by_shared_readers)
            dot_path = os.path.abspath("also_likes.dot")

            # Try to render to PNG using Graphviz if available
            png_path = os.path.abspath("also_likes.png")
            try:
                subprocess.run(
                    ["dot", "-Tpng", dot_path, "-o", png_path],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                self.write_output(
                    "Task 6  Also-likes graph generated.\n\n"
                    f"DOT file: {dot_path}\n"
                    f"PNG file: {png_path}\n\n"
                    "Open the PNG file to view the graph."
                )
            except Exception:
                self.write_output(
                    "Task 6  Also-likes DOT file generated.\n\n"
                    f"DOT file: {dot_path}\n"
                    "Install Graphviz and run:\n"
                    "  dot -Tpng also_likes.dot -o also_likes.png\n"
                    "to create an image of the graph."
                )
        except Exception as exc:
            self.write_output(f"Error in task 6:\n{exc}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AnalyticsGUI(root)
    root.mainloop()


