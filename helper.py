import json
import yaml
import sys
import re
import os
from functools import lru_cache


@lru_cache(maxsize=None)
def load_datapackage(working_directory):
    """Loads the datapackage.json file and caches the result."""
    print(working_directory)
    DATAPACKAGE_FILE = os.path.join(working_directory, "Setup\datapackage.json") 
    with open(DATAPACKAGE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

@lru_cache(maxsize=None)
def item_list(base_game, working_directory):
    """Returns all headers from 'item_name_to_id' in 'Stardew Valley'."""
    if base_game == "The Wind Waker":
        base_game = "Wind Waker"
    data = load_datapackage(working_directory)
    stardew_data = data["games"].get(base_game, {})
    return list(stardew_data.get("item_name_to_id", {}).keys())  # Return as list

@lru_cache(maxsize=None)
def location_list(base_game, working_directory):
    """Returns all headers from 'location_name_to_id' in 'Stardew Valley'."""
    if base_game == "The Wind Waker":
        base_game = "Wind Waker"
    data = load_datapackage(working_directory)
    stardew_data = data["games"].get(base_game, {})
    return list(stardew_data.get("location_name_to_id", {}).keys())

@lru_cache(maxsize=None)
def get_headers(category_type, base_game, working_directory):
    """Returns all headers from either 'item_name_groups' or 'location_name_groups' in 'Stardew Valley'."""
    if base_game == "The Wind Waker":
        base_game = "Wind Waker"
    data = load_datapackage(working_directory)
    stardew_data = data["games"].get(base_game, {})

    if category_type == "item":
        return list(stardew_data.get("item_name_groups", {}).keys())
    elif category_type == "location":
        return list(stardew_data.get("location_name_groups", {}).keys())
    return []

def snake_to_title(text):
    """Convert snake_case to Capital Case (replace underscores with spaces, capitalize words)."""
    return re.sub(r'_+', ' ', text).title()

def title_to_snake(text):
    """Convert Title Case to snake_case (replace spaces with underscores, lowercase words)."""
    return re.sub(r'\s+', '_', text).lower()

def read_yaml(file_path):
    """Reads a YAML file and returns the parsed data."""
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)
