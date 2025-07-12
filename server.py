# server.py
import asyncio
import websockets
import uuid
import json
import os
import random
import typing
from paths import get_exe_folder
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

async def fetch_and_save_datapackage(player_name, game_name, port):
    print("Server Attempt")
    urls_to_try = [
        port,                   # Try as provided
        f"ws://{port}",         # Try with ws://
        f"wss://{port}"         # Try with wss://
    ]

    for websocket_url in urls_to_try:
        try:
            print(f"[server] [INFO] Trying to connect to {websocket_url}...")
            async with websockets.connect(websocket_url) as websocket:
                # Send Connect packet (no password)
                connect_packet = [{
                    'cmd': 'Connect',
                    'password': '',
                    'game': game_name,
                    'name': player_name,
                    'uuid': str(uuid.uuid4()),
                    'version': {'major': 0, 'minor': 6, 'build': 1, "class": "Version"},
                    'items_handling': 7,
                    'tags': ['AP', 'TextOnly', 'GetDatapackage'],
                    'slot_data': False
                }]
                await websocket.send(encode(connect_packet))
                print(f"[server] [INFO] Connected to {websocket_url}")

                # Listen for packets
                while True:
                    message = await websocket.recv()
                    packets = decode(message)
                    for packet in packets:
                        if packet.get("cmd") == "DataPackage":
                            save_datapackage(packet)
                            print("[INFO] DataPackage saved. Disconnecting.")
                            return
                        elif packet.get("cmd") == "RoomInfo":
                            await websocket.send(encode([{"cmd": "GetDataPackage", "games": [game_name]}]))
        except Exception as e:
            print(f"[server] [WARNING] Failed to connect to {websocket_url}: {e}")
    print("[ERROR] Unable to connect using any method.")

def save_datapackage(packet):
    output_dir = os.path.join(get_exe_folder(), "Datapackages")
    os.makedirs(output_dir, exist_ok=True)
    random_number = random.randint(1000, 9999)
    output_path = os.path.join(output_dir, f"datapackage_{random_number}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(packet, f, indent=2)
    print(f"[server] [INFO] Saved to {output_path}")