import yaml
import os
import tkinter as tk
from tkinter import filedialog

def read_yaml(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

def detect_format(data, base_game):
    """Detect if the YAML data is in 'simple' or 'detailed' format."""
    if base_game in data:
        num_detailed_keys = sum(
            1 for value in data[base_game].values()
            if isinstance(value, dict) and value and all(isinstance(v, (int, float)) for v in value.values())
        )
        num_total_keys = len(data[base_game])
        
        # If most dictionaries contain numeric values, classify as detailed
        if num_detailed_keys > num_total_keys / 2:
            return "detailed"
    return "simple"

def convert_yaml(data, base_game, target_format=None):
    detailed_yaml_file_name = "BaseYAMLS/" + base_game + ".yaml"  # Main YAML
    format_type = detect_format(data, base_game)
    print(f"Detected format: {format_type}")
    
    if target_format and format_type == target_format:
        print(f"File is already in {target_format} format. No conversion needed.")
        return data
    
    if format_type == "detailed":
        return detailed_to_simple(data, base_game)
    else:
        detailed_base = read_yaml(detailed_yaml_file_name)  # Load detailed base template
        return simple_to_detailed(data, detailed_base, base_game)

import json  # Ensure json module is imported

def detailed_to_simple(detailed_data, base_game):
    simple_data = {
        "name": detailed_data.get("name", "Player{number}"),
        "description": detailed_data.get("description", "Default The Wind Waker Template"),
        "game": detailed_data.get("game", base_game),
        "requires": detailed_data.get("requires", {}),
        base_game: {}
    }
    
    for key, value in detailed_data.get(base_game, {}).items():
        if isinstance(value, dict) and value:
            chosen_option = max(value, key=value.get)
            simple_data[base_game][key] = chosen_option
        else:
            simple_data[base_game][key] = value

    print("🔹 Converted Detailed to Simple:")
    print(json.dumps(simple_data, indent=4))

    return simple_data

def simple_to_detailed(simple_data, base_data, base_game):
    detailed_data = {
        "name": simple_data.get("name", "Player{number}"),
        "description": simple_data.get("description", "Default The Wind Waker Template"),
        "game": simple_data.get("game", base_game),
        "requires": simple_data.get("requires", {}),
        base_game: base_data.get(base_game, {}).copy()
    }
    
    for key, value in simple_data.get(base_game, {}).items():
        if key in detailed_data[base_game] and isinstance(detailed_data[base_game][key], dict):
            if isinstance(value, dict):
                detailed_data[base_game][key] = value.copy()
            else:
                for option in detailed_data[base_game][key]:
                    detailed_data[base_game][key][option] = 0  
                
                if isinstance(value, str):
                    detailed_data[base_game][key][value] = 50  

        else:
            if isinstance(detailed_data[base_game].get(key), list) and isinstance(value, str):
                detailed_data[base_game][key] = [value]  # Convert single item to list
            else:
                detailed_data[base_game][key] = value

    print("🔹 Converted Simple to Detailed:")
    print(json.dumps(detailed_data, indent=4))

    return detailed_data

