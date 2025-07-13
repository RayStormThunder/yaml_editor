from paths import get_exe_folder
import os
import yaml
import re
import shutil
import config  # To access debug_flag
from path_fixer import sanitize_path_component
from PySide6.QtWidgets import QRadioButton, QVBoxLayout, QButtonGroup
from spacer_utils import move_spacer

def move_yaml_files(main_window, yaml_base_folder):
    for file in os.listdir(yaml_base_folder):
        if file.lower().endswith(".yaml"):
            file_path = os.path.join(yaml_base_folder, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                if isinstance(data, dict) and "game" in data:
                    game_name = str(data["game"])
                    game_name = sanitize_path_component(game_name)
                    game_folder = os.path.join(yaml_base_folder, game_name)
                    os.makedirs(game_folder, exist_ok=True)
                    main_window.moved_yaml_mapping[file] = game_name

                    target_filename = f"{game_name}_Template.yaml"
                    target_path = os.path.join(yaml_base_folder, target_filename)

                    if file != target_filename:
                        if os.path.exists(os.path.join(yaml_base_folder, f"{game_name}_Template.yaml")):
                            # Target {game}.yaml already exists, move this file into game folder without renaming
                            dest_path = os.path.join(game_folder, file)
                            shutil.move(file_path, dest_path)
                            continue  # Skip further processing
                        else:
                            # Rename to {game}_Template.yaml
                            new_path = os.path.join(yaml_base_folder, target_filename)
                            os.rename(file_path, new_path)
                            file_path = new_path
                            file = target_filename

                    # Identify keys to convert
                    game_data = data.get(game_name, {})
                    replacements = []
                    for key, value in list(game_data.items()):
                        if isinstance(value, (str, int, float)):
                            pattern = re.compile(
                                rf'^(\s*){re.escape(key)}:\s*{re.escape(str(value))}(?:\s*#.*)?$', re.MULTILINE
                            )
                            replacements.append((pattern, key, value))

                    # Do text replacement with indentation
                    if replacements:
                        with open(file_path, 'r', encoding='utf-8') as f_in:
                            text = f_in.read()

                        for pattern, key, value in replacements:
                            match = pattern.search(text)
                            if match:
                                indent = match.group(1)
                                replacement = f"{indent}{key}:\n{indent}  {value}: 50"
                                text = pattern.sub(replacement, text)
                                if config.debug_flag:
                                    print(f"[game_and_slot_setup] [INFO] Replaced '{key}: {value}' with block in '{file}'")
                            else:
                                if config.debug_flag:
                                    print(f"[game_and_slot_setup] [WARNING] Could not find match for '{key}: {value}' in '{file}'")

                        with open(file_path, 'w', encoding='utf-8') as f_out:
                            f_out.write(text)

                    # Always copy to the game folder as {game}.yaml
                    dest_path = os.path.join(game_folder, f"{game_name}.yaml")
                    shutil.copy2(file_path, dest_path)

            except Exception as e:
                print(f"[game_and_slot_setup] [ERROR] Unexpected error processing {file_path}: {e}")
                        
def scan_game_names(yaml_base_folder):
    game_names = set()
    for folder in os.listdir(yaml_base_folder):
        folder_path = os.path.join(yaml_base_folder, folder)
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                if file.lower().endswith(".yaml"):
                    file_path = os.path.join(folder_path, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = yaml.safe_load(f)
                            if isinstance(data, dict) and "game" in data:
                                game_names.add(str(data["game"]))
                    except Exception as e:
                        print(f"[game_and_slot_setup] [WARNING] Failed to load {file_path}: {e}")
    return sorted(game_names)

def rebuild_game_buttons(main_window, game_names, prev_game):
    scroll_game_widget = main_window.ui.ScrollGame.widget()
    game_layout = scroll_game_widget.layout()

    if not hasattr(main_window, 'game_group'):
        main_window.game_group = QButtonGroup(main_window)
        main_window.game_group.setExclusive(True)

    current_buttons = [btn.text() for btn in main_window.game_group.buttons()]
    game_changed = current_buttons != game_names

    if game_changed:
        clear_layout(scroll_game_widget)
        main_window.game_group = QButtonGroup(main_window)
        main_window.game_group.setExclusive(True)

        for game_name in game_names:
            button = QRadioButton(game_name)
            game_layout.addWidget(button)
            main_window.game_group.addButton(button)
            if game_name == prev_game:
                button.setChecked(True)

        def on_game_changed():
            selected_game = get_selected_button(main_window.game_group)
            if selected_game:
                refresh_slots(main_window, selected_game, None)

        main_window.game_group.buttonClicked.connect(lambda _: on_game_changed())
        move_spacer(game_layout)

    selected_game = get_selected_button(main_window.game_group)
    if not selected_game and game_names:
        selected_game = game_names[0]
        for btn in main_window.game_group.buttons():
            if btn.text() == selected_game:
                btn.setChecked(True)
                break
        selected_game = get_selected_button(main_window.game_group)

    return game_changed, selected_game

def get_latest_modification_time(folder):
    latest_time = os.path.getmtime(folder)
    for root, dirs, files in os.walk(folder):
        for name in files:
            if name.lower().endswith('.yaml'):
                file_path = os.path.join(root, name)
                latest_time = max(latest_time, os.path.getmtime(file_path))
    return latest_time

def slots_need_refresh(main_window, yaml_base_folder):
    last_modified = get_latest_modification_time(yaml_base_folder) if os.path.exists(yaml_base_folder) else None
    prev_modified = getattr(main_window, 'prev_slot_modified_time', None)
    if prev_modified != last_modified:
        main_window.prev_slot_modified_time = last_modified
        return True
    return False

def refresh_games_and_slots(main_window, prev_game, prev_slot, override):
    yaml_base_folder = os.path.join(get_exe_folder(), "YAMLS")
    os.makedirs(yaml_base_folder, exist_ok=True)
    modification = slots_need_refresh(main_window, yaml_base_folder)

    if modification or override:
        main_window.moved_yaml_mapping = {}
        move_yaml_files(main_window, yaml_base_folder)

        game_names = scan_game_names(yaml_base_folder)
        game_changed, selected_game = rebuild_game_buttons(main_window, game_names, prev_game)

        if selected_game:
            refresh_slots(main_window, selected_game, prev_slot)

        selected_slot = get_selected_button(main_window.slot_group) if hasattr(main_window, 'slot_group') else None
        main_window.current_yaml_path = os.path.join(yaml_base_folder, sanitize_path_component(selected_game), selected_slot) if selected_game and selected_slot else None

        return selected_game, selected_slot
    else:
        return prev_game, prev_slot

def refresh_slots(main_window, selected_game, prev_slot):
    yaml_folder = os.path.join(get_exe_folder(), "YAMLS", sanitize_path_component(selected_game))
    scroll_slot_widget = main_window.ui.ScrollSlot.widget()
    slot_layout = scroll_slot_widget.layout()

    if not os.path.exists(yaml_folder):
        return

    yaml_files = sorted([
        f for f in os.listdir(yaml_folder)
        if f.lower().endswith(".yaml")
    ])

    current_buttons = [btn.text() for btn in getattr(main_window, 'slot_group', QButtonGroup()).buttons()]
    if current_buttons != yaml_files:
        clear_layout(scroll_slot_widget)
        main_window.slot_group = QButtonGroup(main_window)
        main_window.slot_group.setExclusive(True)

        for yaml_file in yaml_files:
            button = QRadioButton(yaml_file)
            slot_layout.addWidget(button)
            main_window.slot_group.addButton(button)
            if yaml_file == prev_slot:
                button.setChecked(True)

    # Auto-select fallback if nothing selected
    if not get_selected_button(main_window.slot_group) and yaml_files:
        main_window.slot_group.buttons()[0].setChecked(True)
    move_spacer(slot_layout)

def get_selected_button(button_group):
    for button in button_group.buttons():
        if button.isChecked():
            return button.text()
    return None

def clear_layout(widget):
    layout = widget.layout()
    if layout is not None:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()