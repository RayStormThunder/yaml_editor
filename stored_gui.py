import json
import os
from PySide6.QtCore import QObject, Signal
from paths import get_gui_data_file

class GlobalSettings(QObject):
    changed = Signal(str, object)  # key, new value

    def __init__(self):
        super().__init__()
        self._cache = {}

    def emit_if_changed(self, key, value):
        old_value = self._cache.get(key)
        if old_value != value:
            self._cache[key] = value
            self.changed.emit(key, value)

# Singleton instance
global_settings = GlobalSettings()

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
    old_value = data.get("Global", {}).get(key)
    if old_value != value:
        data.setdefault("Global", {})[key] = value
        save_gui_data(data)
        global_settings.emit_if_changed(key, value)

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
