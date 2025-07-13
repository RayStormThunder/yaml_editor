import os
import json
import config
import requests
import time
from datetime import datetime
from paths import get_exe_folder  # You already use this

def extract_datapackages():
    base_folder = os.path.join(get_exe_folder(), "Datapackages")
    output_folder = os.path.join(base_folder, "Extracted_Datapackages")
    os.makedirs(base_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    # Get list of JSON files, sorted by oldest modified time first
    json_files = [
        os.path.join(base_folder, f)
        for f in os.listdir(base_folder)
        if f.endswith(".json")
    ]
    json_files.sort(key=lambda f: os.path.getmtime(f))  # Oldest first

    for file_path in json_files:
        file_name = os.path.basename(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"[datapackage_conversion] [ERROR] Invalid JSON in {file_name}, skipping...")
                continue

            games = data.get("games", {})
            for game_name, game_data in games.items():
                game_output_folder = os.path.join(output_folder, game_name)
                os.makedirs(game_output_folder, exist_ok=True)

                item_groups = game_data.get("item_name_groups", {})
                location_groups = game_data.get("location_name_groups", {})
                item_names = list(game_data.get("item_name_to_id", {}).keys())
                location_names = list(game_data.get("location_name_to_id", {}).keys())

                with open(os.path.join(game_output_folder, "item_name_groups.json"), 'w', encoding='utf-8') as out_f:
                    json.dump(item_groups, out_f, indent=2, ensure_ascii=False)

                with open(os.path.join(game_output_folder, "location_name_groups.json"), 'w', encoding='utf-8') as out_f:
                    json.dump(location_groups, out_f, indent=2, ensure_ascii=False)

                with open(os.path.join(game_output_folder, "item_names.json"), 'w', encoding='utf-8') as out_f:
                    json.dump(item_names, out_f, indent=2, ensure_ascii=False)

                with open(os.path.join(game_output_folder, "location_names.json"), 'w', encoding='utf-8') as out_f:
                    json.dump(location_names, out_f, indent=2, ensure_ascii=False)

                if config.debug_flag:
                    print(f"[datapackage_conversion] [INFO] Extracted data for game '{game_name}' from '{file_name}'.")

def get_extracted_data(game, data_type, group=None):
    base_folder = os.path.join(get_exe_folder(), "Datapackages", "Extracted_Datapackages")
    file_map = {
        "item_groups": "item_name_groups.json",
        "location_groups": "location_name_groups.json",
        "item_names": "item_names.json",
        "location_names": "location_names.json"
    }

    if data_type not in file_map:
        raise ValueError(f"[ERROR] Invalid data_type '{data_type}'. Must be one of {list(file_map.keys())}")

    exact_match = None
    partial_match_folder_in_game = None
    partial_match_game_in_folder = None

    for folder in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder)
        if not os.path.isdir(folder_path):
            continue

        if folder == game:
            exact_match = folder
            break
        elif folder in game:
            partial_match_folder_in_game = folder
        elif game in folder:
            partial_match_game_in_folder = folder

    # Prioritize matches
    selected_folder = (
        exact_match or
        partial_match_folder_in_game or
        partial_match_game_in_folder
    )

    if not selected_folder:
        raise FileNotFoundError(f"[ERROR] No matching folder found for game: '{game}' in {base_folder}")

    # Load file
    file_path = os.path.join(base_folder, selected_folder, file_map[data_type])
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"[ERROR] File not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if data_type in ["item_groups", "location_groups"]:
        if group and group != "N/A":
            return data.get(group, [])
        else:
            return list(data.keys())
    else:
        return data

def update_datapackage():
    if config.debug_flag:
        print("[datapackage_conversion] [DEBUG] Starting datapackage update")

    base_folder = os.path.join(get_exe_folder(), "Datapackages")
    if config.debug_flag:
        print(f"[datapackage_conversion] [DEBUG] Base folder: {base_folder}")
    os.makedirs(base_folder, exist_ok=True)

    save_path = os.path.join(base_folder, "datapackage.json")
    version_path = os.path.join(base_folder, "datapackage_version.txt")
    github_url = "https://api.github.com/repos/ArchipelagoMW/Archipelago/releases/latest"
    package_url = "https://archipelago.gg/datapackage"

    try:
        if config.debug_flag:
            print("[datapackage_conversion] [DEBUG] Sending request to GitHub...")
        resp = requests.get(github_url)
        if config.debug_flag:
            print(f"[datapackage_conversion] [DEBUG] GitHub response status: {resp.status_code}")

        if resp.status_code != 200:
            print(f"[datapackage_conversion] [ERROR] Failed to check latest Archipelago version: {resp.status_code}")
            return

        latest_tag = resp.json().get("tag_name", "").strip()
        if config.debug_flag:
            print(f"[datapackage_conversion] [DEBUG] Latest tag: {latest_tag}")

        current_tag = ""
        if os.path.exists(version_path):
            with open(version_path, "r", encoding="utf-8") as f:
                current_tag = f.read().strip()
        if config.debug_flag:
            print(f"[datapackage_conversion] [DEBUG] Current local tag: {current_tag}")

        if latest_tag == current_tag:
            print(f"[datapackage_conversion] [INFO] Datapackage is up to date with tag: {latest_tag}")
            return

        if config.debug_flag:
            print(f"[datapackage_conversion] [INFO] New version available: {latest_tag}")

        response = requests.get(package_url)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            with open(version_path, "w", encoding="utf-8") as f:
                f.write(latest_tag)
            print(f"[datapackage_conversion] [INFO] Datapackage updated to version: {latest_tag}")
        else:
            print(f"[datapackage_conversion] [ERROR] Failed to download datapackage: {response.status_code}")
        extract_datapackages()

    except Exception as e:
        print(f"[datapackage_conversion] [ERROR] Exception occurred: {e}")
