import yaml
import os
import re
import json
import tkinter as tk
import math
from tkinter import ttk
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QStringListModel, QSortFilterProxyModel
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QPushButton, QHBoxLayout, QFileDialog, QMessageBox

from tooltips import TooltipButton
from yaml_converter import convert_yaml
from helper import (
    load_datapackage, item_list, location_list, 
    get_headers, snake_to_title, title_to_snake, read_yaml
)
from themes import dark_theme, notebook_style

selected = {"item": None}  # Global dictionary to track last clicked item
base_game = "Stardew Valley"
detailed_yaml_file_name = "BaseYAMLS/" + base_game + ".yaml"  # Main YAML
included_items = []
excluded_items = []
last_selected_list = None  # Tracks the last clicked list (either "included" or "excluded")
res = ""
res_old = None  # Store last resolution
drag_timer = QtCore.QTimer()  # Timer for detecting drag stop
drag_timer.setSingleShot(True)  # Runs only once per stop

def load_yaml_action(window):
    """Opens a file dialog to load a YAML file and updates the UI."""
    file_dialog = QFileDialog(window)
    file_dialog.setFileMode(QFileDialog.ExistingFile)
    file_dialog.setNameFilter("YAML Files (*.yaml *.yml)")
    file_dialog.setViewMode(QFileDialog.Detail)

    yaml_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "YAML"))
    if os.path.exists(yaml_folder):
        file_dialog.setDirectory(yaml_folder)
    else:
        print(f"Warning: YAML directory {yaml_folder} not found.")

    if file_dialog.exec_():
        selected_files = file_dialog.selectedFiles()
        if selected_files:
            file_path = selected_files[0]
            print(f"Selected YAML file: {file_path}")

            try:
                data = read_yaml(file_path)
                
                # Extract base_game from the YAML data
                global base_game
                base_game = data.get("game", "Unknown")  # Default to "Unknown" if not found
                global detailed_yaml_file_name
                detailed_yaml_file_name = "BaseYAMLS/" + base_game + ".yaml"  # Main YAML
                print(f"Base game set to: {base_game}")

                converted_data = convert_yaml(data, base_game, target_format="detailed")

                global included_items, excluded_items, selected
                included_items = []
                excluded_items = []
                selected = {"item": None}

                old_layout = window.layout()
                if old_layout:
                    while old_layout.count():
                        item = old_layout.takeAt(0)
                        if item.widget():
                            item.widget().deleteLater()
                    QtWidgets.QWidget().setLayout(old_layout)

                create_editor(window, converted_data)  

            except Exception as e:
                QtWidgets.QMessageBox.critical(window, "Error", f"Failed to load YAML file: {str(e)}")


def save_yaml_action(root, reference_data):
    """Saves the extracted UI data into a YAML file, maintaining the original order and confirming the save."""
    extracted_data = extract_ui_data(root, reference_data)

    global base_game
    # Ensure output directory exists
    yaml_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "YAML"))
    os.makedirs(yaml_folder, exist_ok=True)

    # Generate file name from 'name' field
    base_game_add_underscore = base_game.replace(" ", "_")
    file_name = extracted_data["name"].replace(" ", "_") + "-" + base_game_add_underscore + ".yaml"
    file_path = os.path.join(yaml_folder, file_name)

    # Save as YAML while maintaining order
    with open(file_path, "w", encoding="utf-8") as file:
        yaml.dump(extracted_data, file, default_flow_style=False, sort_keys=False)

    # Confirm file saved
    QMessageBox.information(root, "Save Successful", f"YAML file saved successfully:\n{file_path}")

    # Print confirmation & file contents
    print(f"✅ YAML saved successfully: {file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        print(file.read())  # Print saved YAML content to console

def extract_ui_data(root, reference_data):
    """Extracts all user input data from the UI and preserves order based on reference_data."""
    extracted_data = {
        "name": root.findChild(QtWidgets.QLineEdit, "name_entry").text().strip(),
        "description": root.findChild(QtWidgets.QLineEdit, "desc_entry").text().strip(),
        "game": root.findChild(QtWidgets.QLineEdit, "game_entry").text().strip(),
        "requires": reference_data.get("requires", {}),
        base_game: {}
    }

    # Preserve order for general tab
    for category in reference_data[base_game]:
        widget = root.findChild(QtWidgets.QComboBox, f"dropdown_{category}")
        if widget:
            extracted_data[base_game][category] = title_to_snake(widget.currentText())

    # Preserve order for lists, but handle `start_inventory` differently
    for tab in included_items:
        tab_name = tab["tab_name"]
        items = tab["items"]

        if tab_name in reference_data[base_game]:
            if tab_name in ("start_inventory", "start_inventory_from_pool", "starting_items"):
                inventory_dict = {}
                for item in items:
                    inventory_dict[item] = inventory_dict.get(item, 0) + 1
                extracted_data[base_game][tab_name] = inventory_dict
            else:
                extracted_data[base_game][tab_name] = items

    return extracted_data

def return_filter_array(selected_group, current_items):
    """Filters the current items based on the selected dropdown group in both item_name_groups and location_name_groups.
       Always filters out 'Mods' unless 'Mods' is explicitly selected."""
    
    data = load_datapackage()
    stardew_data = data["games"].get(base_game, {})

    # Get both item groups and location groups
    item_groups = stardew_data.get("item_name_groups", {})
    location_groups = stardew_data.get("location_name_groups", {})

    # If "All" is selected, apply default filtering rules
    if selected_group == "All":
        filtered_items = current_items
    else:
        # Get items from both groups if they exist
        matching_items = item_groups.get(selected_group, []) + location_groups.get(selected_group, [])
        filtered_items = [item for item in current_items if item in matching_items]

    # Always filter out "Mods" unless "Mods" is explicitly selected
    if selected_group != "Mods":
        mods_list = item_groups.get("Mods", [])
        filtered_items = [item for item in filtered_items if item not in mods_list]

    # Always filter out "Mods" unless "Mods" is explicitly selected
    if selected_group != "Mods":
        mods_location_list = location_groups.get("Mods", [])
        filtered_items = [item for item in filtered_items if item not in mods_location_list]

    return filtered_items

def extract_comments_before_label(file_path, target_label):
    """Extracts comments appearing before the specified label in a YAML file."""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    found_label = False
    extracted_comments = []

    for i, line in enumerate(lines):
        stripped_line = line.strip()

        # Check for the target label at the start of a line
        if re.match(rf"^{re.escape(target_label)}\s*:", stripped_line):
            found_label = True
            extracted_comments = []  # Reset in case comments are above another label

        # If we found the label, capture all preceding comments
        elif found_label:
            if stripped_line.startswith("#"):
                extracted_comments.append(stripped_line)
            elif stripped_line:  # Stop if we encounter a non-comment line
                break

    return "\n".join(extracted_comments) if extracted_comments else "No comments found."

def create_editor(root, data):
    root.setStyleSheet(dark_theme)
    settings_group = QtWidgets.QGroupBox("")

    # THIS CREATES THE GENERAL TAB
    create_settings_header(data, settings_group)

    old_notebook = root.findChild(QtWidgets.QTabWidget)
    if old_notebook:
        old_notebook.deleteLater()

    notebook = QtWidgets.QTabWidget()
    notebook.setObjectName("general_tab")
    notebook.setStyleSheet(notebook_style)

    # Ensure the QTabWidget resizes properly
    notebook.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
    notebook.setMinimumSize(800, 600)  # Prevent it from shrinking too much

    # Create tabs dynamically
    create_general_tab(data, notebook)
    create_other_tab(data, root, notebook)

    # Button Layout
    button_layout = QHBoxLayout()
    load_button = QPushButton("LOAD YAML")
    save_button = QPushButton("SAVE YAML")  # Placeholder for now

    load_button.clicked.connect(lambda: load_yaml_action(root))  # Hook up LOAD YAML button
    save_button.clicked.connect(lambda: save_yaml_action(root, data))

    button_layout.addWidget(load_button)
    button_layout.addWidget(save_button)

    main_layout = QtWidgets.QVBoxLayout()
    main_layout.addWidget(settings_group)
    main_layout.addWidget(notebook)
    main_layout.addLayout(button_layout)  # Add button row at the bottom

    # Ensure notebook resizes dynamically
    notebook.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

    root.setLayout(main_layout)

    # Force an initial resize to match the window
    root.resize(root.width(), root.height())

def create_settings_header(data, settings_group):
    settings_layout = QtWidgets.QGridLayout()

    name_label = QtWidgets.QLabel("Name:")
    name_entry = QtWidgets.QLineEdit()
    name_entry.setObjectName("name_entry")
    name_entry.setText(data.get("name", ""))

    desc_label = QtWidgets.QLabel("Description:")
    desc_entry = QtWidgets.QLineEdit()
    desc_entry.setObjectName("desc_entry")
    desc_entry.setText(data.get("description", ""))

    game_label = QtWidgets.QLabel("Game:")
    game_entry = QtWidgets.QLineEdit()
    game_entry.setObjectName("game_entry")
    game_entry.setText(snake_to_title(data.get("game", "")))

    settings_layout.addWidget(name_label, 0, 0)
    settings_layout.addWidget(name_entry, 0, 1)
    settings_layout.addWidget(desc_label, 0, 2)
    settings_layout.addWidget(desc_entry, 0, 3)
    settings_layout.addWidget(game_label, 0, 6)
    settings_layout.addWidget(game_entry, 0, 7)

    settings_group.setLayout(settings_layout)

def create_general_tab(data, notebook):
    yaml_file = os.path.join("SettingsFormatting", f"{base_game}.yaml")
    
    if not os.path.exists(yaml_file) or os.stat(yaml_file).st_size == 0:
        print(f"YAML file not found or is empty: {yaml_file}. Creating General tab with all data.")
        create_tab("General", list(data.get(base_game, {}).keys()), data, notebook, base_game, detailed_yaml_file_name)
        return
    
    with open(yaml_file, 'r') as file:
        yaml_content = yaml.safe_load(file) or {}
    
    all_defined_categories = set()
    for tab_name, categories in yaml_content.items():
        if isinstance(categories, list):  # Ensure categories is a list
            all_defined_categories.update(categories)
        else:
            print(f"Warning: Categories for tab '{tab_name}' are not in list format: {categories}")
        create_tab(tab_name, categories, data, notebook, base_game, detailed_yaml_file_name)
    
    print(f"All defined categories: {all_defined_categories}")  # Debugging output
    
    # Find extra categories not listed in any tab
    extra_categories = [category for category in data.get(base_game, {}) if category not in all_defined_categories]
    
    if extra_categories:
        print(f"Categories in General tab: {extra_categories}")  # Debugging output
        create_tab("General", extra_categories, data, notebook, base_game, detailed_yaml_file_name)

def create_tab(tab_name, categories, data, notebook, base_game, detailed_yaml_file_name):
    tab = QtWidgets.QWidget()
    layout = QtWidgets.QGridLayout()
    layout.setSpacing(0)  # Reduce spacing between widgets
    
    tooltips = {category: extract_comments_before_label(detailed_yaml_file_name, category) for category in categories}
    
    row, col = 0, 0
    for category, content in data.get(base_game, {}).items():
        if isinstance(content, dict) and all(isinstance(v, (int, float)) for v in content.values()):
            if not content:
                continue

            if category in ["start_inventory", "start_inventory_from_pool", "starting_items"]:  
                continue  # Skip processing start_inventory

            if category not in categories:
                continue  # Skip if category is not listed under the current tab header

            frame = QtWidgets.QWidget()
            frame_layout = QtWidgets.QVBoxLayout()
            frame_layout.setSpacing(0)  # Reduce spacing in the frame

            label_row = QtWidgets.QHBoxLayout()
            label_row.setSpacing(0)  # Reduce spacing in the frame

            label = QtWidgets.QLabel(snake_to_title(category) + ":")
            tooltip_text = tooltips.get(category, "No comments found.")
            tooltip_button = TooltipButton(tooltip_text, frame)

            label_row.addWidget(label)
            label_row.addStretch()
            label_row.addWidget(tooltip_button, alignment=Qt.AlignRight)

            dropdown = QtWidgets.QComboBox()
            dropdown.setObjectName(f"dropdown_{category}")
            dropdown.setEditable(True)
            dropdown.setMaxVisibleItems(40)

            selected_value = snake_to_title(str(max(content, key=content.get)))
            options = [snake_to_title(str(k)) for k in content.keys()]
            dropdown.addItems(options)

            frame_layout.addLayout(label_row)
            frame_layout.addWidget(dropdown)
            frame.setLayout(frame_layout)

            layout.addWidget(frame, row, col, 1, 2)

            if selected_value in options:
                dropdown.setCurrentText(selected_value)

            col += 2
            if col >= 10:
                row += 1
                col = 0
    
    tab.setLayout(layout)
    notebook.addTab(tab, tab_name)


def create_other_tab(data, root, notebook):
    category_data = data.get(base_game, {})
    tab_data = {}
    #print(base_game)
    #print(category_data)
    initial_order = {}  # Stores the original order of items

    

    for category, content in category_data.items():
        if isinstance(content, dict): 
            if content and all(isinstance(v, int) for v in content.values()):
                if not any(c in category for c in ["start_inventory","start_inventory_from_pool", "starting_items"]):  
                    pass  
                else:
                    content = [item for item, count in content.items() for _ in range(count)]
            else:
                content = []

        if isinstance(content, list):
            item_list_array = item_list(base_game)
            location_list_array = location_list(base_game)
            dropdown_options = []
            


            included_items.append({"tab_name": category, "items": content})
            excluded_items.append({"tab_name": category, "items": []})

            #GENERAL
            if category in ["local_items", "non_local_items", "start_hints", "item_links", "start_inventory", "starting_items", "start_inventory_from_pool"]:
                excluded_items[-1]["items"] = item_list_array  # Updates the last appended excluded_items entry
                dropdown_options = get_headers("item", base_game)

            if category in ["start_location_hints", "priority_locations", "exclude_locations"]:
                excluded_items[-1]["items"] = location_list_array  # Updates the last appended excluded_items entry
                dropdown_options = get_headers("location", base_game)

            if not category in ["start_inventory", "start_inventory_from_pool", "starting_items"]:
                excluded_items[-1]["items"] = [item for item in excluded_items[-1]["items"] if item not in content]

            #STARDEW VALLEY
            if category == "walnutsanity":                
                excluded_items[-1]["items"] = ["Bushes", "Dig Spot", "Puzzles", "Repeatables"]

            if category == "enabled_filler_buffs":                
                excluded_items[-1]["items"] = ["Bite Rate", "Damage", "Defense", "Energy", "Fish Trap", "Fishing Bar Size", "Health", "Immunity", "Luck"]

            if category == "mods":                
                excluded_items[-1]["items"] = ["Alec Revisited", "Alecto the Witch", "Archaeology", "Ayeisha - The Postal Worker (Custom NPC)", "Bigger Backpack", "Binning Skill", "Distant Lands - Witch Swamp Overhaul",
                                                "Hat Mouse Lacey", "Juna - Roomate NPC", "Luck Skill", "Mister Ginger (cat npc)", "Professor Jasper Thomas", "Skull Cavern Elevator", "Socializing Skill", "Stardew Valley Expanded",
                                                "Tractor Mod"]

            # **SKIP TAB CREATION IF BOTH INCLUDED & EXCLUDED ARE EMPTY**
            if not included_items[-1]["items"] and not excluded_items[-1]["items"]:
                included_items.pop()  # Remove the last added entry
                excluded_items.pop()  # Remove the last added entry
                continue  # Skip creating this tab




            tab_data[category] = {"included": content, "excluded": []}

            tab_frame = QtWidgets.QWidget()
            tab_layout = QtWidgets.QHBoxLayout()

            included_layout = QtWidgets.QVBoxLayout()

            included_search_row = QtWidgets.QHBoxLayout()
            # Only add the dropdown if dropdown_options is not empty
            if dropdown_options:
                included_dropdown = QtWidgets.QComboBox()
                included_dropdown.addItems(["All"] + dropdown_options)  # Add "All" as a default option
                included_dropdown.setMaxVisibleItems(40)  # Adjust number of visible items
                included_dropdown.setObjectName(f"included_dropdown_{category}")
                included_dropdown.currentIndexChanged.connect(refresh_lists)  # Call refresh when selection changes
                included_search_row.addWidget(included_dropdown)
            included_search = QtWidgets.QLineEdit()
            included_search.setPlaceholderText("Search Selected")
            included_search.setObjectName(f"included_search_{category}")
            included_search_row.addWidget(included_search)

            included_list = QtWidgets.QListWidget()
            included_list.setObjectName(f"included_list_{category}")



            excluded_layout = QtWidgets.QVBoxLayout()

            excluded_search_row = QtWidgets.QHBoxLayout()
            # Only add the dropdown if dropdown_options is not empty
            if dropdown_options:
                excluded_dropdown = QtWidgets.QComboBox()
                excluded_dropdown.addItems(["All"] + dropdown_options)  # Add "All" as a default option
                excluded_dropdown.setMaxVisibleItems(40)  # Adjust number of visible items
                excluded_dropdown.setObjectName(f"excluded_dropdown_{category}")
                excluded_dropdown.currentIndexChanged.connect(refresh_lists)  # Call refresh when selection changes
                excluded_search_row.addWidget(excluded_dropdown)
            excluded_search = QtWidgets.QLineEdit()
            excluded_search.setPlaceholderText("Search Unselected")
            excluded_search.setObjectName(f"excluded_search_{category}")
            excluded_search_row.addWidget(excluded_search)
            
            excluded_list = QtWidgets.QListWidget()
            excluded_list.setObjectName(f"excluded_list_{category}")

            included_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
            excluded_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

            def refresh_lists():
                current_tab_name = notebook.tabText(notebook.currentIndex())
                current_tab_name_formatted = title_to_snake(current_tab_name)

                # Find UI elements
                included_list_widget = root.findChild(QtWidgets.QListWidget, f"included_list_{current_tab_name_formatted}")
                excluded_list_widget = root.findChild(QtWidgets.QListWidget, f"excluded_list_{current_tab_name_formatted}")

                included_search_widget = root.findChild(QtWidgets.QLineEdit, f"included_search_{current_tab_name_formatted}")
                excluded_search_widget = root.findChild(QtWidgets.QLineEdit, f"excluded_search_{current_tab_name_formatted}")

                included_dropdown_widget = root.findChild(QtWidgets.QComboBox, f"included_dropdown_{current_tab_name_formatted}")
                excluded_dropdown_widget = root.findChild(QtWidgets.QComboBox, f"excluded_dropdown_{current_tab_name_formatted}")

                # Get selected group from dropdown
                included_selected_group = included_dropdown_widget.currentText() if included_dropdown_widget else "All"
                excluded_selected_group = excluded_dropdown_widget.currentText() if excluded_dropdown_widget else "All"

                # Get included/excluded arrays for the selected tab
                included_array = [tab["items"] for tab in included_items if tab["tab_name"] == current_tab_name_formatted]
                excluded_array = [tab["items"] for tab in excluded_items if tab["tab_name"] == current_tab_name_formatted]

                # Flatten lists
                included_array = [item for sublist in included_array for item in sublist]
                excluded_array = [item for sublist in excluded_array for item in sublist]

                # Store original order of all items when first encountered
                for index, item in enumerate(excluded_array + included_array):  # Process both lists
                    if item not in initial_order:
                        initial_order[item] = index  # Store its original position

                # Apply filtering based on dropdown selection
                included_array = return_filter_array(included_selected_group, included_array)
                excluded_array = return_filter_array(excluded_selected_group, excluded_array)

                # Get search text
                included_search_text = included_search_widget.text().strip().lower() if included_search_widget else ""
                excluded_search_text = excluded_search_widget.text().strip().lower() if excluded_search_widget else ""

                # Apply search filtering
                filtered_included = [item for item in included_array if included_search_text in item.lower()]
                filtered_excluded = [item for item in excluded_array if excluded_search_text in item.lower()]

                # Sort both included and excluded based on initial_order
                filtered_included.sort(key=lambda item: initial_order.get(item, float('inf')))  # Default to last if missing
                filtered_excluded.sort(key=lambda item: initial_order.get(item, float('inf')))  # Default to last if missing

                # Update list widgets with filtered results
                if isinstance(included_list_widget, QtWidgets.QListWidget):
                    included_list_widget.clear()
                    included_list_widget.addItems(filtered_included)

                if isinstance(excluded_list_widget, QtWidgets.QListWidget):
                    excluded_list_widget.clear()
                    excluded_list_widget.addItems(filtered_excluded)



            # Call refresh_lists when the tab is changed
            def on_tab_change():
                refresh_lists()

            included_search.setObjectName(f"included_search_{category}")
            excluded_search.setObjectName(f"excluded_search_{category}")

            included_search.textChanged.connect(refresh_lists)
            excluded_search.textChanged.connect(refresh_lists)

            # Trigger refresh when the tab changes
            notebook.currentChanged.connect(on_tab_change)

            refresh_lists()  # Initial refresh when creating the UI

            # Create a single toggle button
            toggle_button = QtWidgets.QPushButton("<- Move ->")
            toggle_button.setMinimumHeight(50)  # Adjust as needed
            toggle_button.setMaximumHeight(100)  # Adjust as needed

            def move_selected_items():
                """Move selected items between lists dynamically."""
                if "items" not in selected or not isinstance(selected["items"], list):
                    selected["items"] = []  # Ensure it's always initialized as a list

                if not selected["items"]:
                    return

                current_tab_name = notebook.tabText(notebook.currentIndex())
                current_tab_name_formatted = title_to_snake(current_tab_name)

                included_list_widget = root.findChild(QtWidgets.QListWidget, f"included_list_{current_tab_name_formatted}")
                excluded_list_widget = root.findChild(QtWidgets.QListWidget, f"excluded_list_{current_tab_name_formatted}")

                # Determine source list based on selection
                if included_list_widget and included_list_widget.selectedItems():
                    source_list = "included"
                    dest_list = "excluded"
                elif excluded_list_widget and excluded_list_widget.selectedItems():
                    source_list = "excluded"
                    dest_list = "included"
                else:
                    return  # No valid selection

                print(f"(move_selected_items) Moving items from {source_list} to {dest_list}: {selected['items']}")

                is_start_inventory = current_tab_name_formatted in ("start_inventory", "start_inventory_from_pool", "starting_items")

                for item_name in selected["items"]:
                    if source_list == "excluded":  # Move from Excluded to Included
                        for tab in excluded_items:
                            if tab["tab_name"] == current_tab_name_formatted and item_name in tab["items"]:
                                if not is_start_inventory:
                                    tab["items"].remove(item_name)
                                break
                        for tab in included_items:
                            if tab["tab_name"] == current_tab_name_formatted:
                                tab["items"].append(item_name)
                                break

                    elif source_list == "included":  # Move from Included to Excluded
                        for tab in included_items:
                            if tab["tab_name"] == current_tab_name_formatted and item_name in tab["items"]:
                                tab["items"].remove(item_name)
                                break
                        for tab in excluded_items:
                            if tab["tab_name"] == current_tab_name_formatted:
                                if not is_start_inventory:
                                    tab["items"].append(item_name)
                                break

                refresh_lists()

            # Connect the toggle button
            toggle_button.clicked.connect(move_selected_items)

            # Add the single button to the layout
            button_layout = QtWidgets.QVBoxLayout()
            button_layout.addWidget(toggle_button)


            button_layout = QtWidgets.QVBoxLayout()
            button_layout.addWidget(toggle_button)

            # Add the search rows to their respective layouts
            included_layout.addLayout(included_search_row)
            included_layout.addWidget(included_list)
            excluded_layout.addLayout(excluded_search_row)
            excluded_layout.addWidget(excluded_list)
            
            tab_layout.addLayout(included_layout)
            tab_layout.addLayout(button_layout)
            tab_layout.addLayout(excluded_layout)
            
            tab_frame.setLayout(tab_layout)
            notebook.addTab(tab_frame, snake_to_title(category))

            def item_clicked(source_list):
                """Handles selection of multiple items in the currently active list."""
                global last_selected_list

                current_tab_name = notebook.tabText(notebook.currentIndex())
                current_tab_name_formatted = title_to_snake(current_tab_name)

                included_list_widget = root.findChild(QtWidgets.QListWidget, f"included_list_{current_tab_name_formatted}")
                excluded_list_widget = root.findChild(QtWidgets.QListWidget, f"excluded_list_{current_tab_name_formatted}")

                # If switching lists, clear the previous selection
                if last_selected_list and last_selected_list != source_list:
                    if last_selected_list == "included" and included_list_widget:
                        included_list_widget.clearSelection()
                    elif last_selected_list == "excluded" and excluded_list_widget:
                        excluded_list_widget.clearSelection()

                # Update last selected list
                last_selected_list = source_list

                selected_items = []

                if source_list == "included" and included_list_widget:
                    selected_items.extend(included_list_widget.selectedItems())
                elif source_list == "excluded" and excluded_list_widget:
                    selected_items.extend(excluded_list_widget.selectedItems())

                # Store selected item texts
                selected["items"] = [item.text() for item in selected_items]

                print(f"(item_clicked) Selected ({source_list}): {selected['items']}")


            def clear_selection():
                """Clears the selection if focus is lost, but keeps it if interacting with buttons"""
                focused_widget = QtWidgets.QApplication.instance().focusWidget()

                # Allow interactions with toggle_button without clearing selection
                if isinstance(focused_widget, (QtWidgets.QPushButton, QtWidgets.QListWidget)):
                    if focused_widget == toggle_button:
                        return  # Don't clear selection when clicking the toggle button
                    return  # Don't clear selection if interacting with buttons or lists

                if selected["item"]:
                    print("(clear_selection) Selection cleared due to focus loss.")
                    selected["item"] = None


            # Connect focusChanged signal to clear selection when clicking outside
            QtWidgets.QApplication.instance().focusChanged.connect(lambda old, new: clear_selection() if new else None)

            included_list.itemSelectionChanged.connect(lambda: item_clicked("included"))
            excluded_list.itemSelectionChanged.connect(lambda: item_clicked("excluded"))
            included_list.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            excluded_list.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

def get_screen_resolution_2(window):
    """Returns the true resolution of the screen where the window is displayed, accounting for DPI scaling."""
    screen = window.screen()
    if screen:
        native_size = screen.geometry()  # Get full resolution of the current screen
        device_pixel_ratio = screen.devicePixelRatio()  # Account for OS scaling
        logical_dpi = screen.logicalDotsPerInch() / 96.0  # Normalize DPI (96 is standard)
        
        # Get true (physical) screen resolution
        true_width = int(native_size.width() * device_pixel_ratio / logical_dpi)
        true_height = int(native_size.height() * device_pixel_ratio / logical_dpi)

        return true_width, true_height, native_size  # Return true resolution and geometry
    return None, None, None  # Return None if screen is not found

def adjust_window_size(window):
    """ Adjusts the window size dynamically based on the current screen resolution """
    print("Resize")
    
    screen_width, screen_height, screen_geometry = get_screen_resolution_2(window)
    
    if screen_width is None or screen_height is None or screen_geometry is None:
        print("Error: Could not determine screen resolution.")
        return
    
    width = (-(screen_width/(1.5*3840))+1)
    width = math.floor(width * 10) / 10
    print("Screen Width: " + str(screen_width))
    print("Width Scaler: " + str(width))

    window_width = int(screen_width * width)   # 25% of screen width
    window_height = int(screen_height * 0.25)  # 25% of screen height

    # Get the current screen's position (prevents moving to primary monitor)
    screen_x = screen_geometry.x()  # X position of the current screen
    screen_y = screen_geometry.y()  # Y position of the current screen

    # Center the window **on the current screen**, not the primary screen
    window_x = screen_x + (screen_width - window_width) // 6
    window_y = screen_y + (screen_height - window_height) // 8  # Centered vertically

    window.setGeometry(window_x, window_y, window_width, window_height)

def get_screen_resolution(window):
    """Returns the true resolution of the screen where the window is displayed, accounting for DPI scaling."""
    screen = window.screen()
    if screen:
        native_size = screen.geometry()
        device_pixel_ratio = screen.devicePixelRatio()
        true_width = int(native_size.width() * device_pixel_ratio)
        true_height = int(native_size.height() * device_pixel_ratio)
        return f"True Screen Resolution: {true_width}x{true_height}"
    return "Screen not found"

def update_screen_resolution(window):
    """Updates the resolution only when it changes."""
    global res_old
    res_new = get_screen_resolution(window)

    if res_old != res_new:
        res_old = res_new
        print("Current Resolution Workspace Changes To: " + res_new)
        adjust_window_size(window)

def moveEvent(event):
    """Called when the window moves. Starts a timer to detect when dragging stops."""
    drag_timer.start(500)  # Restart timer with 500ms delay

def main(new_file_path=None, converted_data=None):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication([])

    window = QtWidgets.QWidget()
    window.setWindowTitle("YAML Editor")

    adjust_window_size(window)  # Initial size adjustment

    # Connect move event and drag timer
    window.moveEvent = moveEvent
    drag_timer.timeout.connect(lambda: update_screen_resolution(window))

    # Detect when the window moves to a new screen
    window_window = window.windowHandle()
    if window_window:
        window_window.screenChanged.connect(lambda: (adjust_window_size(window), update_screen_resolution(window)))

    # Print initial screen resolution
    update_screen_resolution(window)

    file_path = new_file_path if new_file_path else detailed_yaml_file_name

    if converted_data:
        data = converted_data
    else:
        if not os.path.exists(file_path):
            print("Error: YAML file not found. Exiting.")
            return
        data = read_yaml(file_path)

    create_editor(window, data)

    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
