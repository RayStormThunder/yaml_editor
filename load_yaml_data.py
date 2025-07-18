import yaml
import re
import os
import config
from add_rows import clear_all_rows, add_both_rows
from tab_manager import clear_tabs, add_tabs_for_game
from paths import get_exe_folder
from PySide6.QtWidgets import QWidget

def load_yaml_file(yaml_path):
    if os.path.exists(yaml_path):
        with open(yaml_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    else:
        print(f"[load_yaml_data] [WARNING] No YAML found at '{yaml_path}'.")
        return {}

def extract_comments(yaml_path, selected_game_name):
    with open(yaml_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    comments = {}
    current_key = None
    for line in lines:
        if line.strip().startswith("#"):
            comment = line.strip().lstrip("#").strip()
            if current_key:
                comments.setdefault(current_key, []).append(comment)
        elif re.match(r'^\s*\w+:', line):
            match = re.match(r'^\s*(\w+):', line)
            if match:
                current_key = match.group(1)
    return comments

def resolve_selected_option(value):
    if isinstance(value, dict):
        if value:
            return str(max(value, key=lambda k: value[k]))
    elif isinstance(value, (str, int, float)):
        return str(value)
    return None

def prepare_row_data(base_yaml_path, selected_game_path, selected_game_name):
    # Load both YAML files
    base_yaml_data = load_yaml_file(base_yaml_path)
    selected_yaml_data = load_yaml_file(selected_game_path)

    # Extract section from both
    base_game_data = base_yaml_data.get(selected_game_name)
    selected_game_values = selected_yaml_data.get(selected_game_name, {})

    if not base_game_data:
        print(f"[load_yaml_data] [ERROR] Game '{selected_game_name}' not found in base YAML.")
        return None, []

    comments = extract_comments(base_yaml_path, selected_game_name)

    row_data = []

    for name, base_options in base_game_data.items():
        if isinstance(base_options, dict):
            description = "\n".join(comments.get(name, []))
            # Start with base options
            final_options = {str(k): int(v) for k, v in base_options.items()}
            # Store the original base values from base YAML before applying selected values
            original_options = final_options.copy()

            if name in selected_game_values:
                selected_value = selected_game_values[name]

                # Set all values to 0 initially
                for k in final_options:
                    final_options[k] = 0

                if isinstance(selected_value, dict):
                    for k, v in selected_value.items():
                        if int(v) != 0:
                            final_options[str(k)] = int(v)
                else:
                    # Single selected option -> set it to 50
                    if str(selected_value) in final_options:
                        final_options[str(selected_value)] = 50
                    else:
                        final_options[str(selected_value)] = 50

                # If all values are 0, restore original base values
                if all(v == 0 for v in final_options.values()):
                    final_options = original_options

            # Determine base_yaml_selected (option with 50 in base YAML)
            base_yaml_selected = None
            for option_name, value in base_options.items():
                if value == 50:
                    base_yaml_selected = str(option_name)
                    break

            # Determine selected_yaml_selected (highest weighted option)
            selected_yaml_selected = None
            max_value = max(final_options.values(), default=None)
            if max_value is not None:
                for option_name, value in final_options.items():
                    if value == max_value:
                        selected_yaml_selected = str(option_name)
                        break

            original_selected = None
            if name in selected_game_values:
                selected_value = selected_game_values[name]
                if isinstance(selected_value, str):
                    original_selected = selected_value
                elif isinstance(selected_value, dict):
                    for k, v in selected_value.items():
                        if int(v) == 50:
                            original_selected = str(k)
                            break

            row_data.append({
                "name": name,
                "items": final_options,  # merged with selected
                "description": description,
                "base_yaml_selected": base_yaml_selected,
                "selected_yaml_selected": selected_yaml_selected,
                "base_items_dict": original_options,
                "original_selected": original_selected
            })

    return (base_yaml_path, selected_game_path), row_data

def load_yaml_UI(main_window, base_yaml_path, selected_game_path, selected_game_name):
    paths, rows = prepare_row_data(base_yaml_path, selected_game_path, selected_game_name)
    if not rows:
        return

    # Load main fields from the selected YAML
    selected_yaml_data = load_yaml_file(selected_game_path)
    main_fields = ["name", "description", "game"]
    for field in main_fields:
        if field in selected_yaml_data:
            if field == "name":
                main_window.ui.NameLineEdit.setText(str(selected_yaml_data[field]))
            elif field == "description":
                description = str(selected_yaml_data[field])
                if "default" in description.lower() or "template" in description.lower() or "example" in description.lower() or "generated" in description.lower():
                    description = "Generated by RayStormThunder's YAML Editor"
                main_window.ui.DescriptionLineEdit.setText(description)
            elif field == "game":
                main_window.ui.GameLineEdit.setText(str(selected_yaml_data[field]))

    # Set YAMLLineEdit based on file name prefix or "name" field
    yaml_filename = os.path.basename(selected_game_path)
    suffix = f"-{selected_game_name}.yaml"
    if yaml_filename.endswith(suffix):
        yaml_prefix = yaml_filename[:-len(suffix)]
        main_window.ui.YAMLLineEdit.setText(yaml_prefix)
    else:
        # Fallback: use the 'name' field from the YAML
        name_value = selected_yaml_data.get("name", "")
        main_window.ui.YAMLLineEdit.setText(str(name_value))
 

    base_yaml_data = load_yaml_file(base_yaml_path)
    game_data = base_yaml_data.get(selected_game_name, {})
    if config.debug_flag:
        print(f"[load_yaml_data] game_data Is: {game_data}")

    clear_tabs(main_window)
    # Gets list of items that are tabs, not to be added to "general"
    tabbed_keys = add_tabs_for_game(main_window, game_data, selected_game_path, selected_game_name)

    if config.debug_flag:
        print(f"[load_yaml_data] tabbed_keys Is: {tabbed_keys}")

    # Print the paths (once, globally)
    if config.debug_flag:
        print(paths[0])
        print(paths[1])

    # Clear previous rows and initialize template_items from base_yaml
    clear_all_rows(main_window)

    # Populate template_items from base (template) only
    main_window.template_items = {}
    main_window.template_items_keys = {}
    main_window.template_items_full = {}
    for row in rows:
        name = row["name"]
        base_items = row.get("base_items_dict", {})
        main_window.template_items[name] = list(base_items.keys())  # for normal rows
        main_window.template_items_keys[name] = list(base_items.keys())  # for normal rows
        main_window.template_items_full[name] = base_items.copy()        # for weighted rows

    for row in rows:
        if row["name"] in tabbed_keys:
            continue  # Skip rows that were added as tabs

        if config.debug_flag:
            print(f"[load_yaml_data] {row['name']} Value Is:")
            print(f"[load_yaml_data] [base_yaml_path]: {row['base_yaml_selected']}")
            print(f"[load_yaml_data] [selected_path]: {row['selected_yaml_selected']}")
            print(f"[load_yaml_data] [items]: {row['items']}")

        add_both_rows(
            main_window,
            name=row["name"],
            items=row["items"],
            description=row["description"],
            starting_item=row["selected_yaml_selected"],
            original_selected=row["original_selected"],
            base_yaml_selected=row["base_yaml_selected"]
        )
    
    from add_rows import setup_row_style_signal

    setup_row_style_signal(
        main_window.ui.ScrollMain,
        main_window.template_items,
        main_window.template_items_full,
        main_window.row_data
    )

