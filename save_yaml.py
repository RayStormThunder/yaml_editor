import yaml
import os
from PySide6.QtWidgets import QListView
from collections import Counter
from paths import get_exe_folder
from load_yaml_data import load_yaml_file
from stored_gui import set_yaml_setting
from path_fixer import sanitize_path_component

def convert_to_yaml_format(data):
    """Converts Python data to a formatted YAML string."""
    return yaml.dump(data, sort_keys=False, allow_unicode=True)

def save_yaml(main_window):
    # Step 1: Load the base YAML
    has_rows = False
    for i in range(main_window.ui.ScrollMain.widget().layout().count()):
        row = main_window.ui.ScrollMain.widget().layout().itemAt(i).widget()
        if row:
            has_rows = True
            break

    if not has_rows:
        # No YAML loaded  Fetch DataPackage instead
        name = main_window.ui.NameLineEdit.text()
        game = main_window.ui.GameLineEdit.text()
        port = main_window.ui.DescriptionLineEdit.text()
        from server import fetch_and_save_datapackage
        import asyncio
        asyncio.run(fetch_and_save_datapackage(name, game, port))
        return  # Done
    else:
        selected_game = main_window.ui.GameLineEdit.text()
        clean_selected_game = sanitize_path_component(selected_game)
        base_yaml_path = os.path.join(get_exe_folder(), "YAMLS", f"{clean_selected_game}_Template.yaml")

        if not os.path.exists(base_yaml_path):
            print(f"[save_yaml] [ERROR] Base YAML not found: {base_yaml_path}")
            return

        base_yaml = load_yaml_file(base_yaml_path)

        # Step 2: Get NameLineEdit and GameLineEdit values
        name_value = main_window.ui.NameLineEdit.text()
        yaml_name_value = main_window.ui.YAMLLineEdit.text()
        game_value = main_window.ui.GameLineEdit.text()

        # Step 3: Create new YAML data (starting from base_yaml)
        new_yaml = base_yaml.copy()  # Copy to avoid modifying base_yaml directly

        # Step 4: Update the 'name' field in new_yaml
        new_yaml['name'] = name_value

        # Step 5: Check WeightedSettingsEnabled checkbox
        weighted_enabled = main_window.ui.WeightedSettingsEnabled.isChecked()
        
        # Step 6: Apply values
        if weighted_enabled:
            set_weighted_values(main_window, new_yaml, game_value)
        else:
            set_normal_values(main_window, new_yaml, game_value)

        for i in range(main_window.ui.MainTabs.count()):
            tab_name = main_window.ui.MainTabs.tabText(i)
            if tab_name == "General":
                continue  # Skip General tab

            tab = main_window.ui.MainTabs.widget(i)
            tab_type = tab.property("tab_type")  # ← READ TYPE HERE

            include_list = tab.findChild(QListView, "IncludeList")
            if not include_list or tab_type is None:
                continue  # Skip if missing

            # Read list values
            model = include_list.model()
            values = [model.data(model.index(j, 0)) for j in range(model.rowCount())]

            # Handle based on type
            if tab_type == "list":
                set_game_option(new_yaml, game_value, tab_name, values)
            elif tab_type == "dict":
                counted = dict(Counter(values))
                set_game_option(new_yaml, game_value, tab_name, counted)

        clean_game_value = sanitize_path_component(game_value)

        output_dir = os.path.join(get_exe_folder(), "YAMLS", clean_game_value)
        os.makedirs(output_dir, exist_ok=True)  # Create directory if missing

        output_path = os.path.join(output_dir, f"{yaml_name_value}-{clean_game_value}.yaml")
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(new_yaml, f, sort_keys=False, allow_unicode=True)

        yaml_key = f"{name_value}-{clean_game_value}.yaml"
        set_yaml_setting(yaml_key, "Enter Weighted Option Mode", weighted_enabled)

        print(f"[save_yaml] [INFO] Saved YAML to: {output_path}")

def set_normal_values(main_window, new_yaml, game_value):
    for i in range(main_window.ui.ScrollMain.widget().layout().count()):
        row = main_window.ui.ScrollMain.widget().layout().itemAt(i).widget()
        if not row or getattr(row, "row_type", None) != "normal":
            continue
        from PySide6.QtWidgets import QLabel, QComboBox

        label = row.findChild(QLabel, "SettingLabel")
        combo = row.findChild(QComboBox, "SettingSimpleCombo")

        if label and combo:
            field_name = label.text()
            selected_value = combo.currentText()
            set_game_option(new_yaml, game_value, field_name, selected_value)

def set_weighted_values(main_window, new_yaml, game_value):
    print("[DEBUG] Running set_weighted_values...")

    from PySide6.QtWidgets import QLabel, QLineEdit, QSpinBox

    for i in range(main_window.ui.ScrollMain.widget().layout().count()):
        row = main_window.ui.ScrollMain.widget().layout().itemAt(i).widget()
        if not row or getattr(row, "row_type", None) != "weighted":
            continue

        label = row.findChild(QLabel, "Name")
        if not label:
            continue

        field_name = label.text()
        weighted_dict = {}

        # Loop through all sub-rows inside SubRowHolder (sub_row_holder)
        sub_widgets = [row.sub_row_holder.itemAt(j).widget() for j in range(row.sub_row_holder.count())]

        for sub in sub_widgets:
            key_input = sub.findChild(QLineEdit, "SpecificSettingName")
            val_spin = sub.findChild(QSpinBox, "SpecificSettingNumber")

            if key_input and val_spin:
                key = key_input.text()
                value = val_spin.value()
                weighted_dict[key] = value

        # Save the collected dictionary
        set_game_option(new_yaml, game_value, field_name, weighted_dict)

def set_game_option(yaml_data, game_key, field_name, value):
    """Sets a field under the given game header in the YAML data.
    Supports auto-converting single choice into weighted dict."""
    if game_key not in yaml_data:
        yaml_data[game_key] = {}

    if isinstance(value, dict) or isinstance(value, list):
        yaml_data[game_key][field_name] = value
    else:
        # Auto-convert: set 50 to selected, 0 to others
        existing_field = yaml_data[game_key].get(field_name, {})
        if isinstance(existing_field, dict):
            new_dict = {}
            for k in existing_field.keys():
                new_dict[k] = 50 if str(k) == str(value) else 0
            # Add value if not present yet
            if str(value) not in new_dict:
                new_dict[str(value)] = 50
            yaml_data[game_key][field_name] = new_dict
        else:
            # Fallback: just set as value (for safety)
            yaml_data[game_key][field_name] = value