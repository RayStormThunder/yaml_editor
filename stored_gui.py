import json
import os
from paths import get_gui_data_file

def load_gui_data():
    """Loads the GUI data JSON file, returns empty dict if missing or corrupted."""
    try:
        with open(get_gui_data_file(), "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_gui_data(data):
    """Saves the GUI data to disk."""
    with open(get_gui_data_file(), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_global_setting(key, default=None):
    data = load_gui_data()
    return data.get("Global", {}).get(key, default)


def set_global_setting(key, value):
    data = load_gui_data()
    data.setdefault("Global", {})[key] = value
    save_gui_data(data)


def get_game_setting(game_name, key, default=None):
    data = load_gui_data()
    return data.get("Games", {}).get(game_name, {}).get(key, default)


def set_game_setting(game_name, key, value):
    data = load_gui_data()
    data.setdefault("Games", {}).setdefault(game_name, {})[key] = value
    save_gui_data(data)


def get_yaml_setting(yaml_name, key, default=None):
    data = load_gui_data()
    return data.get("YAMLs", {}).get(yaml_name, {}).get(key, default)


def set_yaml_setting(yaml_name, key, value):
    data = load_gui_data()
    data.setdefault("YAMLs", {}).setdefault(yaml_name, {})[key] = value
    save_gui_data(data)
