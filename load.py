import json

def load_data(file_path):
    with open(file_path, "r") as f:
        for line in f:
            if line != '\n':
                yield json.loads(line)