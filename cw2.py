import argparse
import sys
import tkinter as tk
from guiVer1 import AnalyticsGUI
from task2 import run_task_2a, run_task_2b
from task3 import run_task_3a, run_task_3b
from task4 import run_task_4
from task5 import run_task_5d
from task6 import run_task_6


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="F21SC CW2 command-line interface"
    )
    parser.add_argument(
        "-u",
        "--user_uuid",
        help="Visitor UUID (used by tasks 6 and 7)",
        default=None,
    )
    parser.add_argument(
        "-d",
        "--doc_uuid",
        help="Document UUID (required for most tasks)",
        default=None,
    )
    parser.add_argument(
        "-t",
        "--task_id",
        required=True,
        help="Task id: 2a, 2b, 3a, 3b, 4, 5d, 6, 7",
    )
    parser.add_argument(
        "-f",
        "--file_name",
        default="issuu_cw2.json",
        help="Input JSON file (default: issuu_cw2.json)",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    task = args.task_id.lower()
    doc = args.doc_uuid
    user = args.user_uuid
    file_path = args.file_name


    needs_doc = {"2a", "2b", "3a", "3b", "4", "5d", "6"}
    if task in needs_doc and not doc:
        print("Error: -d / --doc_uuid is required for this task.", file=sys.stderr)
        return 1

    if task == "2a":
        run_task_2a(file_path, doc)
    elif task == "2b":
        run_task_2b(file_path, doc)
    elif task == "3a":
        run_task_3a(file_path, doc)
    elif task == "3b":
        run_task_3b(file_path, doc)
    elif task == "4":
        run_task_4(file_path, doc)
    elif task == "5d":
        run_task_5d(file_path, doc)
    elif task == "6":
        if not user:
            print(
                "Error: -u / --user_uuid is required for task 6.",
                file=sys.stderr,
            )
            return 1
        png_path = run_task_6(file_path, doc, user)
        print("Also-likes graph PNG generated at:")
        print(png_path)
    elif task == "7":
        root = tk.Tk()
        app = AnalyticsGUI(root)
        
        # Pre-fill document and user IDs if provided
        if doc:
            app.doc_entry.insert(0, doc)
        if user:
            app.user_entry.insert(0, user)

        # Optionally, automatically run task 6 so the graph is shown immediately
        if doc:
            try:
                app.run_task("6")
            except Exception:
                # If anything goes wrong, just fall back to interactive GUI
                pass

        root.mainloop()
    else:
        print(f"Unknown task id: {args.task_id}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


