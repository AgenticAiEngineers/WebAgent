import json
import os

try:
    import sqlite3
except Exception:
    sqlite3 = None

DB_PATH = "memory/chat_memory.db"
FALLBACK_PATH = "memory/storage.json"


def _read_fallback_messages():
    if not os.path.exists(FALLBACK_PATH):
        return []

    try:
        with open(FALLBACK_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return []

    if not isinstance(data, list):
        return []

    cleaned = []
    for item in data:
        if isinstance(item, dict) and "role" in item and "content" in item:
            cleaned.append({"role": item["role"], "content": item["content"]})
    return cleaned


def _write_fallback_messages(messages):
    os.makedirs(os.path.dirname(FALLBACK_PATH), exist_ok=True)
    with open(FALLBACK_PATH, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=True, indent=2)


def init_db():
    if sqlite3 is None:
        if not os.path.exists(FALLBACK_PATH):
            _write_fallback_messages([])
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            message TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_message(role, message):
    if sqlite3 is None:
        messages = _read_fallback_messages()
        messages.append({"role": role, "content": message})
        _write_fallback_messages(messages)
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chat_history (role, message) VALUES (?, ?)",
        (role, message)
    )

    conn.commit()
    conn.close()


def load_history():
    if sqlite3 is None:
        return _read_fallback_messages()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT role, message FROM chat_history")
    rows = cursor.fetchall()

    conn.close()

    return [{"role": r, "content": m} for r, m in rows]
