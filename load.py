import json

def load_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f: #encoding added
        for line in f:
            if line != '\n':
                yield json.loads(line)