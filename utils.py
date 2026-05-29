import json
import os
from datetime import datetime

DATA_DIR = "data"
HISTORY_FILE = f"{DATA_DIR}/history.json"
STATS_FILE = f"{DATA_DIR}/stats.json"

DEFAULT_STATS = {
    "total_analyses": 0,
    "python": 0,
    "javascript": 0,
    "java": 0,
    "cpp": 0,
    "sql": 0
}


def _ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def save_history(code, language, mode, result, quality):
    _ensure_data_dir()

    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as f:
            json.dump([], f)

    try:
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    except Exception:
        history = []

    history.insert(0, {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "language": language,
        "mode": mode,
        "code": code,
        "summary": result.get("summary", ""),
        "score": quality["overall"]
    })

    with open(HISTORY_FILE, "w") as f:
        json.dump(history[:20], f, indent=4)


def update_stats(language):
    _ensure_data_dir()

    if not os.path.exists(STATS_FILE):
        stats = DEFAULT_STATS.copy()
    else:
        try:
            with open(STATS_FILE, "r") as f:
                stats = json.load(f)
        except Exception:
            stats = DEFAULT_STATS.copy()

    stats["total_analyses"] += 1

    lang_map = {
        "Python":     "python",
        "JavaScript": "javascript",
        "Java":       "java",
        "C++":        "cpp",
        "SQL":        "sql"
    }

    key = lang_map.get(language)
    if key:
        stats[key] += 1

    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=4)


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def load_stats():
    if not os.path.exists(STATS_FILE):
        return None
    try:
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return None


def reset_all_data():
    _ensure_data_dir()
    with open(STATS_FILE, "w") as f:
        json.dump(DEFAULT_STATS.copy(), f, indent=4)
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)
