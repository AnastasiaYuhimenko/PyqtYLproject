import json
import os

SETTINGS_FILE = "settings.txt"


def init_settings():
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w") as f:
            json.dump({}, f)


def save_setting(key: str, value):
    init_settings()
    with open(SETTINGS_FILE, "r") as f:
        data = json.load(f)
    data[key] = value
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f)


def load_setting(key: str, default=None):
    init_settings()
    with open(SETTINGS_FILE, "r") as f:
        data = json.load(f)
    return data.get(key, default)


def clear_setting(key: str):
    init_settings()
    with open(SETTINGS_FILE, "r") as f:
        data = json.load(f)
    if key in data:
        del data[key]
        with open(SETTINGS_FILE, "w") as f:
            json.dump(data, f)
