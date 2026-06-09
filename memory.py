import json
import os
from typing import List

MEMORY_FILE = "memory.json"
MAX_HISTORY = 20


def _load() -> list[dict]:
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def _save(history: list[dict]) -> None:
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def get_history() -> list[dict]:
    return _load()


def add_message(role: str, content: str | list) -> None:
    history = _load()
    history.append({"role": role, "content": content})
    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]
    _save(history)


def clear_history() -> None:
    _save([])


def get_last_n(n: int = 5) -> list[dict]:
    history = _load()
    return history[-n:]
