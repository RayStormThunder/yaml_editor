# server.py
import asyncio
import websockets
import uuid
import json
import os
import random
import typing
import config
from paths import get_exe_folder
from path_fixer import sanitize_path_component
from datapackage_conversion import extract_datapackages
from json import JSONEncoder

_encode = JSONEncoder(
    ensure_ascii=False,
    check_circular=False,
    separators=(',', ':'),
).encode

def encode(obj: typing.Any) -> str:
    return _encode(_scan_for_TypedTuples(obj))

def decode(message):
    return json.loads(message)

def _scan_for_TypedTuples(obj: typing.Any) -> typing.Any:
    if isinstance(obj, tuple) and hasattr(obj, "_fields"):  # NamedTuple is not actually a parent class
        data = obj._asdict()
        data["class"] = obj.__class__.__name__
        return data
    if isinstance(obj, (tuple, list, set, frozenset)):
        return tuple(_scan_for_TypedTuples(o) for o in obj)
    if isinstance(obj, dict):
        return {key: _scan_for_TypedTuples(value) for key, value in obj.items()}
    return obj

def is_datapackage_checksum_present(game_name, target_checksum):
    datapackages_folder = os.path.join(get_exe_folder(), "Datapackages")
    if not os.path.exists(datapackages_folder):
        return False

    for file in os.listdir(datapackages_folder):
        if file.endswith(".json"):
            try:
                with open(os.path.join(datapackages_folder, file), "r", encoding="utf-8") as f:
                    data = json.load(f)
                    game_data = data.get("games", {}).get(game_name, {})
                    if game_data.get("checksum") == target_checksum:
                        return True
            except Exception as e:
                print(f"[server] [WARNING] Failed to read {file}: {e}")
    return False

async def fetch_and_save_datapackage(player_name, game_name, port):
    print("[server] [Info] Connecting to Server")
    output_dir = os.path.join(get_exe_folder(), "Datapackages")
    os.makedirs(output_dir, exist_ok=True)

    try:
        port_new = str(port).split(":")[-1]
        if not port_new.isdigit():
            raise ValueError
    except Exception:
        print(f"[INFO] Incorrect Server Address")
        return

    output_path = os.path.join(output_dir, f"datapackage_{port_new}.json")
    if os.path.exists(output_path):
        print(f"[INFO] Datapackage for port {port_new} already exists at {output_path}. Skipping fetch.")
        return

    urls_to_try = [
        port,
        f"ws://{port}",
        f"wss://{port}"
    ]

    for websocket_url in urls_to_try:
        try:
            if config.debug_flag:
                print(f"[server] [INFO] Trying to connect to {websocket_url}...")
            async with websockets.connect(websocket_url) as websocket:
                await websocket.send(encode([{
                    'cmd': 'Connect',
                    'password': '',
                    'game': game_name,
                    'name': player_name,
                    'uuid': str(uuid.uuid4()),
                    'version': {'major': 0, 'minor': 6, 'build': 1, "class": "Version"},
                    'items_handling': 7,
                    'tags': ['AP', 'TextOnly'],
                    'slot_data': False
                }]))
                print(f"[server] [INFO] Connected to {websocket_url}")

                # Track when we've received both packets
                got_data_package = False
                got_retrieved_data = False

                while True:
                    message = await websocket.recv()
                    packets = decode(message)

                    for packet in packets:
                        if packet.get("cmd") == "RoomInfo":
                            checksum = packet.get("datapackage_checksums", {}).get(game_name)
                            if not checksum:
                                print(f"[server] [WARNING] No checksum found for game: {game_name}. Verify the correct game name and keep in mind it is case sensitive.")
                                return

                            if config.debug_flag:
                                print(f"[server] [INFO] Received checksum for {game_name}: {checksum}")

                            if is_datapackage_checksum_present(game_name, checksum):
                                print(f"[server] [INFO] Datapackage for '{game_name}' is up to date. Skipping fetch.")
                                return

                            # Send both requests
                            await websocket.send(encode([{"cmd": "GetDataPackage", "games": [game_name]}]))
                            await websocket.send(encode([{
                                "cmd": "Get",
                                "keys": [
                                    f"_read_item_name_groups_{game_name}",
                                    f"_read_location_name_groups_{game_name}"
                                ]
                            }]))

                        elif packet.get("cmd") == "DataPackage":
                            latest_data_packet = packet
                            got_data_package = True
                            if config.debug_flag:
                                print("[server] [INFO] DataPackage received.")

                        elif packet.get("cmd") == "Retrieved":
                            item_group_key = f"_read_item_name_groups_{game_name}"
                            location_group_key = f"_read_location_name_groups_{game_name}"

                            keys_data = packet.get("keys", {})
                            item_groups = keys_data.get(item_group_key)
                            location_groups = keys_data.get(location_group_key)
                            got_retrieved_data = True

                        # After packet processing
                        if got_data_package and got_retrieved_data:
                            save_datapackage(latest_data_packet, game_name, item_groups, location_groups)
                            if config.debug_flag:
                                print("[server] [INFO] All data received. Disconnecting.")
                            return

        except Exception as e:
            if config.debug_flag:
                print(f"[server] [WARNING] Failed to connect to {websocket_url}: {e}")

    if config.debug_flag:
        print("[server] [ERROR] Unable to connect using any method.")

def save_datapackage(packet, game_name, item_groups=None, location_groups=None):
    output_dir = os.path.join(get_exe_folder(), "Datapackages")
    os.makedirs(output_dir, exist_ok=True)

    # Build file path using game name
    safe_game_name = game_name.replace(" ", "_")
    super_safe_game_name = sanitize_path_component(safe_game_name)
    output_path = os.path.join(output_dir, f"datapackage_{super_safe_game_name}.json")

    # Extract the datapackage structure
    data_package = packet.get("data", {})
    games_data = data_package.get("games", {})
    game_entry = None

    # Match game name case-insensitively
    for key in games_data:
        if key.lower() == game_name.lower():
            game_entry = games_data[key]
            break

    if not game_entry:
        print(f"[server] [ERROR] Game '{game_name}' not found in DataPackage.")
        return

    # Insert item and location groups if present
    if item_groups:
        game_entry["item_name_groups"] = item_groups
    if location_groups:
        game_entry["location_name_groups"] = location_groups

    # Build ordered game entry
    ordered_game_entry = {}

    # Insert in desired order
    if "item_name_groups" in game_entry:
        ordered_game_entry["item_name_groups"] = game_entry["item_name_groups"]
    if "item_name_to_id" in game_entry:
        ordered_game_entry["item_name_to_id"] = game_entry["item_name_to_id"]
    if "location_name_groups" in game_entry:
        ordered_game_entry["location_name_groups"] = game_entry["location_name_groups"]
    if "location_name_to_id" in game_entry:
        ordered_game_entry["location_name_to_id"] = game_entry["location_name_to_id"]
    if "checksum" in game_entry:
        ordered_game_entry["checksum"] = game_entry["checksum"]

    # Final structure
    final_data = {
        "games": {
            game_name: ordered_game_entry
        }
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=2)

    print(f"[server] [INFO] Saved datapackage to {output_path}")
    extract_datapackages()
