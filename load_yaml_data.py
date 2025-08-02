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
	base_yaml_data = load_yaml_file(base_yaml_path)
	selected_yaml_data = load_yaml_file(selected_game_path)

	base_game_data = base_yaml_data.get(selected_game_name)
	selected_game_values = selected_yaml_data.get(selected_game_name, {})

	if not base_game_data:
		print(f"[load_yaml_data] [ERROR] Game '{selected_game_name}' not found in base YAML.")
		return None, []

	comments = extract_comments(base_yaml_path, selected_game_name)

	row_data = []
	seen_keys = set()
	base_keys = list(base_game_data.keys())
	insert_index_map = {}

	# Step 1: Process base keys in order
	for i, name in enumerate(base_keys):
		base_options = base_game_data[name]
		if not isinstance(base_options, dict):
			continue

		insert_index_map[name] = len(row_data)  # Record current position
		description = "\n".join(comments.get(name, []))
		final_options = {str(k): int(v) for k, v in base_options.items()}
		original_options = final_options.copy()

		last_touched = "base"
		if name in selected_game_values:
			last_touched = "selected"
			selected_value = selected_game_values[name]
			for k in final_options:
				final_options[k] = 0
			if isinstance(selected_value, dict):
				for k, v in selected_value.items():
					if int(v) != 0:
						final_options[str(k)] = int(v)
			else:
				final_options[str(selected_value)] = 50

			if all(v == 0 for v in final_options.values()):
				final_options = original_options

		base_yaml_selected = next((str(opt) for opt, val in base_options.items() if val == 50), None)
		max_value = max(final_options.values(), default=None)
		selected_yaml_selected = next((str(opt) for opt, val in final_options.items() if val == max_value), None)

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
			"items": final_options,
			"description": description,
			"base_yaml_selected": base_yaml_selected,
			"selected_yaml_selected": selected_yaml_selected,
			"base_items_dict": original_options,
			"original_selected": original_selected,
			"last_touched": last_touched
		})
		seen_keys.add(name)

	# Step 2: Insert removed rows at proper positions
	extra_keys = [key for key in selected_game_values.keys() if key not in seen_keys]

	for extra_key in extra_keys:
		selected_value = selected_game_values[extra_key]
		final_options = {}

		if isinstance(selected_value, dict):
			final_options = {str(k): int(v) for k, v in selected_value.items()}
		elif isinstance(selected_value, str):
			final_options = {str(selected_value): 50}
		else:
			continue  # skip if unexpected type

		selected_yaml_selected = next((str(opt) for opt, val in final_options.items() if val == max(final_options.values(), default=0)), None)

		insert_index = len(row_data)  # default to end

		# Try to insert based on alphabetical order (or numerical order) similarity to base_keys
		for i, base_key in enumerate(base_keys):
			if extra_key < base_key:
				insert_index = i
				break

		removed_row = {
			"name": f"{extra_key}-REMOVED",
			"items": final_options,
			"description": "[Removed from base template]",
			"base_yaml_selected": None,
			"selected_yaml_selected": selected_yaml_selected,
			"base_items_dict": {},
			"original_selected": selected_yaml_selected,
			"last_touched": "removed"
		}

		row_data.insert(insert_index, removed_row)

	# Step 3: Compute merged ordering using base order and selected unique keys
	final_order = base_keys.copy()

	selected_keys = list(selected_game_values.keys())
	extra_keys = [k for k in selected_keys if k not in base_keys]

	for extra_key in extra_keys:
		# Find the previous known key (that exists in base) in selected order
		prev_base_key = None
		for i in range(selected_keys.index(extra_key) - 1, -1, -1):
			if selected_keys[i] in base_keys:
				prev_base_key = selected_keys[i]
				break

		if prev_base_key and prev_base_key in final_order:
			insert_index = final_order.index(prev_base_key) + 1
		else:
			insert_index = len(final_order)

		if extra_key not in final_order:
			final_order.insert(insert_index, extra_key + "-REMOVED")  # renamed for removed

	# Reorder row_data based on final_order
	row_data_dict = {row["name"]: row for row in row_data}
	row_data = [row_data_dict[name] for name in final_order if name in row_data_dict]

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
            base_yaml_selected=row["base_yaml_selected"],
	        last_touched=row.get("last_touched", "base"),
        )
    
    from add_rows import setup_row_style_signal

    setup_row_style_signal(
        main_window.ui.ScrollMain,
        main_window.template_items,
        main_window.template_items_full,
        main_window.row_data
    )

