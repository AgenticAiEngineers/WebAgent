import json
import os

MEMORY_FILE = "memory/storage.json"


def save_memory(key, value):
    if not os.path.exists(MEMORY_FILE):
        data = {}
    else:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)

    data[key] = value

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_memory(key):
    if not os.path.exists(MEMORY_FILE):
        return None

    with open(MEMORY_FILE, "r") as f:
        data = json.load(f)

    return data.get(key, None)
