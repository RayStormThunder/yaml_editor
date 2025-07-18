from PySide6.QtWidgets import QWidget, QListView, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import QStringListModel
from ui_added_removed_lists import Ui_Form
from stored_gui import set_game_setting, get_global_setting, get_game_setting, global_settings
from datapackage_conversion import get_extracted_data
import yaml
import config
from PySide6.QtWidgets import QStyledItemDelegate, QStyle
from PySide6.QtGui import QBrush, QColor
from PySide6.QtCore import Qt

class ColoredItemDelegate(QStyledItemDelegate):
    def __init__(self, get_color_func, parent=None):
        super().__init__(parent)
        self.get_color_func = get_color_func

    def paint(self, painter, option, index):
        color = self.get_color_func(index.data())
        if color and not (option.state & QStyle.State_Selected):
            painter.save()
            painter.fillRect(option.rect, QColor(color))
            painter.restore()

        super().paint(painter, option, index)


def clear_tabs(main_window):
    """Removes all tabs from MainTabs except the 'General' tab."""
    for i in reversed(range(main_window.ui.MainTabs.count())):
        tab_name = main_window.ui.MainTabs.tabText(i)
        if tab_name != "General":
            main_window.ui.MainTabs.removeTab(i)

def add_tabs_for_game(main_window, game_data, selected_game_path, game_name):
    from stored_gui import get_game_setting, set_game_setting  # Safe to reimport here

    always_add_keys = {
        "local_items",
        "non_local_items",
        "start_inventory",
        "start_inventory_from_pool",
        "start_hints",
        "start_location_hints",
        "exclude_locations",
        "priority_locations",
        "item_links"
    }

    items = {
        "local_items",
        "non_local_items",
        "start_hints",
        "start_inventory",
        "start_inventory_from_pool",
        "item_links"
    }

    locations = {
        "start_location_hints",
        "exclude_locations",
        "priority_locations"
    }

    tabbed_keys = set()
    for key, value in game_data.items():
        should_add_tab = False
        if isinstance(value, list):
            should_add_tab = True
        elif isinstance(value, dict) and not value:
            should_add_tab = True
        elif key in always_add_keys:
            should_add_tab = True

        if should_add_tab:
            tab = QWidget()
            tab_ui = Ui_Form()
            tab_ui.setupUi(tab)
            tab_type = "dict" if isinstance(value, dict) else "list"
            tab.setProperty("tab_type", tab_type)  # Store 'list' or 'dict' on the QWidget itself

            # Shared model for exclude
            saved_items = get_game_setting(game_name, "Additional Items In Lists", {}).get(key, [])
            exclude_model = QStringListModel()
            exclude_model.setStringList(saved_items)

            setup_add_remove_button(tab_ui, game_name, key, exclude_model=exclude_model)
            setup_include_exclude_move_button(tab_ui, game_name, tab_type, key, initial_include=[], exclude_model=exclude_model)

            type_field = tab_ui.Type
            type_field.clear()
            type_field.addItems(["Custom", "Item", "Location"])

            # Load saved value if exists, otherwise apply default
            saved_type = get_game_setting(game_name, "Tab Types", {}).get(key)

            if saved_type in {"Custom", "Item", "Location"}:
                type_field.setCurrentText(saved_type)
            else:
                if key in items:
                    type_field.setCurrentText("Item")
                elif key in locations:
                    type_field.setCurrentText("Location")
                else:
                    type_field.setCurrentText("Custom")

            def make_type_changed(tab_ui, game_name, tab_key, exclude_model, selected_game_path):
                def on_type_changed(index):
                    value = tab_ui.Type.currentText()
                    all_types = get_game_setting(game_name, "Tab Types", {})
                    all_types[tab_key] = value
                    set_game_setting(game_name, "Tab Types", all_types)

                    # Re-apply everything (this will clear & refill lists based on type)
                    apply_type_setting(tab_ui, tab_type, game_name, tab_key, value, exclude_model, selected_game_path)

                    # Refresh filter boxes too (now matching new type)
                    populate_filter_boxes(tab_ui, game_name, value)

                    update_type_visibility(tab_ui, tab_key, value, items, locations)
                return on_type_changed


            type_field.currentIndexChanged.connect(
                make_type_changed(tab_ui, game_name, key, exclude_model, selected_game_path)
            )

            apply_type_setting(tab_ui, tab_type, game_name, key, type_field.currentText(), exclude_model, selected_game_path)
            populate_filter_boxes(tab_ui, game_name, type_field.currentText())
            update_type_visibility(tab_ui, key, type_field.currentText(), items, locations)

            # Connect SearchInputInclude, FilterInclude, and FilterExclude to filtering (with live type reading)
            def make_filter_function(tab_ui, game_name):
                def filter_func():
                    current_type = tab_ui.Type.currentText()
                    filter_include_exclude_lists(tab_ui, game_name, current_type)
                return filter_func

            filter_func = make_filter_function(tab_ui, game_name)
            tab_ui.SearchInputInclude.textChanged.connect(filter_func)
            tab_ui.FilterInclude.currentIndexChanged.connect(filter_func)
            tab_ui.FilterExclude.currentIndexChanged.connect(filter_func)


            tab.setStyleSheet("""
                QWidget {
                    background-color: #2c2c2c;
                }
                QComboBox, QLineEdit, QListView, QPushButton {
                    background-color: #1e1e1e;
                    color: #dcdcdc;
                    border: 1px solid #444;
                }
                QPushButton:hover {
                    background-color: #2c2c2c;
                }
                QScrollBar:vertical {
                    width: 4px;
                    background: #2c2c2c;
                    border: none;
                    border-radius: 4px;
                }
                QScrollBar::handle:vertical {
                    background: #5e5e5e;
                    min-height: 20px;
                    border-radius: 4px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #888;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    background: none;
                    height: 0px;
                }
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                    background: none;
                }
            """)
            main_window.ui.MainTabs.addTab(tab, key)
            tabbed_keys.add(key)
            if config.debug_flag:
                print(f"[tab_manager] Key is: {key}")

    return tabbed_keys

def add_list_item(tab_ui, name: str, target_list: str):
    """Adds name to IncludeList or ExcludeList in the tab."""
    if target_list == "IncludeList":
        list_view = tab_ui.IncludeList
    elif target_list == "ExcludeList":
        list_view = tab_ui.ExcludeList
    else:
        return  # Invalid list name

    model = list_view.model()
    if model is None:
        model = QStringListModel()
        list_view.setModel(model)

    current_items = model.stringList()

    if name not in current_items:
        current_items.append(name)
        model.setStringList(sorted(current_items))
        
def apply_type_setting(tab_ui, tab_type, game_name, tab_key, type_value, exclude_model, selected_game_path):
    """Clears lists & applies auto-exclusions for 'Item' and 'Location'."""
    include_model = tab_ui.IncludeList.model()
    if include_model is None:
        include_model = QStringListModel()
        tab_ui.IncludeList.setModel(include_model)

    # Clear both lists
    include_model.setStringList([])
    exclude_model.setStringList([])

    # Load custom saved exclusions from JSON
    saved_items = get_game_setting(game_name, "Additional Items In Lists", {}).get(tab_key, [])
    exclude_model.setStringList(saved_items)

    # Auto-fill for Item / Location
    if type_value == "Item":
        try:
            all_items = get_extracted_data(game_name, "item_names")
            exclude_model.setStringList(sorted(all_items))
        except Exception as e:
            print(f"[tab_manager] [ERROR] Failed to load item names for {game_name}: {e}")

    elif type_value == "Location":
        try:
            all_locations = get_extracted_data(game_name, "location_names")
            exclude_model.setStringList(sorted(all_locations))
        except Exception as e:
            print(f"[tab_manager] [ERROR] Failed to load location names for {game_name}: {e}")

    apply_yaml_items(tab_ui, tab_type, selected_game_path, tab_key, exclude_model)


def setup_add_remove_button(tab_ui, game_name, tab_key, exclude_model):
    tab_ui.ExcludeList.setModel(exclude_model)  # ← Shared model here

    # Load & save remain unchanged because you already passed in saved items
    def save_current_list():
        all_data = get_game_setting(game_name, "Additional Items In Lists", {})
        all_data[tab_key] = exclude_model.stringList()
        set_game_setting(game_name, "Additional Items In Lists", all_data)

    def on_add_remove_clicked():
        text = tab_ui.AddRemoveInput.text().strip()
        if not text:
            return

        items = exclude_model.stringList()
        if text in items:
            items.remove(text)
        else:
            items.append(text)

        exclude_model.setStringList(sorted(items))
        save_current_list()
        tab_ui.AddRemoveInput.clear()

    tab_ui.AddRemoveButton.clicked.connect(on_add_remove_clicked)
    tab_ui.AddRemoveInput.returnPressed.connect(on_add_remove_clicked)

def setup_include_exclude_move_button(tab_ui, game_name, tab_type, tab_key, initial_include=None, exclude_model=None):
    initial_include = initial_include or []
    if exclude_model is None:
        exclude_model = QStringListModel()

    # Shared model applied here
    include_model = QStringListModel()
    tab_ui.IncludeList.setModel(include_model)
    tab_ui.ExcludeList.setModel(exclude_model)

    def get_exclude_item_color(name):

        red_enabled = get_global_setting("RedState", False)
        green_enabled = get_global_setting("GreenState", False)

        additional_items = get_game_setting(game_name, "Additional Items In Lists", {}).get(tab_key, [])

        if name in additional_items:
            if red_enabled:
                return "#5c4e1e"  # red

        if not hasattr(tab_ui, "original_include_counts"):
            return None

        count_original = tab_ui.original_include_counts.get(name, 0)
        count_current = tab_ui.IncludeList.model().stringList().count(name)

        if count_current < count_original:
            if green_enabled:
                return "#1e5c2a"  # green

        return None

    def get_include_item_color(name):
        red_enabled = get_global_setting("RedState", False)
        green_enabled = get_global_setting("GreenState", False)

        if not hasattr(tab_ui, "original_include_counts"):
            return None

        count_original = tab_ui.original_include_counts.get(name, 0)
        count_current = tab_ui.IncludeList.model().stringList().count(name)

        if count_current > count_original and green_enabled:
            return "#1e5c2a"

        additional_items = get_game_setting(game_name, "Additional Items In Lists", {}).get(tab_key, [])
        if name in additional_items and red_enabled:
            return "#5c4e1e"

        return None

    tab_ui.IncludeList.setItemDelegate(ColoredItemDelegate(get_include_item_color, tab_ui.IncludeList))
    tab_ui.ExcludeList.setItemDelegate(ColoredItemDelegate(get_exclude_item_color, tab_ui.ExcludeList))

    # Function to refresh the list views (colors)
    def refresh_list_colors():
        tab_ui.IncludeList.viewport().update()
        tab_ui.ExcludeList.viewport().update()

    # Respond to setting changes
    def on_setting_changed(key, value):
        if key in ("RedState", "GreenState"):
            refresh_list_colors()

    global_settings.changed.connect(on_setting_changed)

    include_model.setStringList(initial_include)

    # Enable multi-selection
    tab_ui.IncludeList.setSelectionMode(QListView.MultiSelection)
    tab_ui.ExcludeList.setSelectionMode(QListView.MultiSelection)

    # Deselect other list when selecting one
    tab_ui.IncludeList.selectionModel().selectionChanged.connect(
        lambda *_: tab_ui.ExcludeList.clearSelection())
    tab_ui.ExcludeList.selectionModel().selectionChanged.connect(
        lambda *_: tab_ui.IncludeList.clearSelection())

    # Move button logic (now both lists share ExcludeList properly)
    def on_move_clicked():
        include_items = include_model.stringList()
        exclude_items = set(exclude_model.stringList())

        selected_include = [index.data() for index in tab_ui.IncludeList.selectedIndexes()]
        selected_exclude = [index.data() for index in tab_ui.ExcludeList.selectedIndexes()]

        if tab_type == "list":
            # Convert to set for fast updates
            include_set = set(include_items)
            for item in selected_include:
                include_set.discard(item)
                exclude_items.add(item)
            for item in selected_exclude:
                exclude_items.discard(item)
                include_set.add(item)
            include_items = sorted(include_set)
        else:  # dict behavior
            # Remove one instance of each selected item from include_items
            for item in selected_include:
                if item in include_items:
                    include_items.remove(item)
            # Add one instance of each selected item to include_items
            include_items.extend(selected_exclude)

        include_model.setStringList(sorted(include_items))
        exclude_model.setStringList(sorted(exclude_items))

        current_type = tab_ui.Type.currentText()
        filter_include_exclude_lists(tab_ui, game_name, current_type)
        tab_ui.IncludeList.viewport().update()
        tab_ui.ExcludeList.viewport().update()


    tab_ui.Move.clicked.connect(on_move_clicked)

def apply_yaml_items(tab_ui, tab_type, yaml_path, key, exclude_model):
    """Move items from YAML to included list, adjusting excluded list based on tab_type."""
    include_model = tab_ui.IncludeList.model()
    if include_model is None:
        include_model = QStringListModel()
        tab_ui.IncludeList.setModel(include_model)

    # Load YAML
    with open(yaml_path, 'r', encoding='utf-8') as f:
        yaml_data = yaml.safe_load(f)

    game_name = yaml_data.get("game")
    if not game_name or game_name not in yaml_data:
        print("[ERROR] Game section missing in YAML")
        return

    game_section = yaml_data[game_name]

    if key not in game_section:
        return  # Nothing to move

    yaml_value = game_section[key]
    include_items = []

    if isinstance(yaml_value, dict):
        for item, count in yaml_value.items():
            try:
                count = int(count)
            except:
                count = 1
            include_items.extend([item] * count)
    elif isinstance(yaml_value, list):
        include_items.extend(yaml_value)

    # Update include list
    include_model.setStringList(sorted(include_items))

    # Update exclude list
    excluded_items = set(exclude_model.stringList())
    if tab_type == "list":
        # Remove items from exclude if they are now included
        for item in include_items:
            excluded_items.discard(item)
    else:  # dict mode — ensure at least 1 copy of each unique item is present in exclude
        unique_items = set(include_items)
        excluded_items.update(unique_items)

    # Track original counts of each item
    tab_ui.original_include_counts = {}
    for item in include_items:
        tab_ui.original_include_counts[item] = tab_ui.original_include_counts.get(item, 0) + 1

    exclude_model.setStringList(sorted(excluded_items))

def populate_filter_boxes(tab_ui, game_name, type_value):
    """Populate FilterInclude and FilterExclude based on type (using datapackage groups)."""
    filter_include = tab_ui.FilterInclude
    filter_exclude = tab_ui.FilterExclude

    # Clear existing items
    filter_include.clear()
    filter_exclude.clear()

    if type_value == "Item":
        try:
            group_names = get_extracted_data(game_name, "item_groups")
            if "Everything" not in group_names:
                group_names.append("Everything")
            group_names_sorted = sorted(name for name in group_names if name != "Everything")
            group_names_sorted.insert(0, "Everything")  # Put 'Everything' at top

            # Add to FilterInclude normally
            filter_include.addItems(group_names_sorted)

            # For FilterExclude, skip "Everything", insert "Nothing" instead
            filter_exclude.addItem("Nothing")
            for name in group_names_sorted[1:]:
                filter_exclude.addItem(name)

        except Exception as e:
            print(f"[tab_manager] [ERROR] Failed to load item groups for {game_name}: {e}")

    elif type_value == "Location":
        try:
            group_names = get_extracted_data(game_name, "location_groups")
            if "Everywhere" not in group_names:
                group_names.append("Everywhere")
            group_names_sorted = sorted(name for name in group_names if name != "Everywhere")
            group_names_sorted.insert(0, "Everywhere")  # Put 'Everywhere' at top

            # Add to FilterInclude normally
            filter_include.addItems(group_names_sorted)

            # For FilterExclude, skip "Everywhere", insert "Nowhere" instead
            filter_exclude.addItem("Nowhere")
            for name in group_names_sorted[1:]:
                filter_exclude.addItem(name)

        except Exception as e:
            print(f"[tab_manager] [ERROR] Failed to load location groups for {game_name}: {e}")

def update_type_visibility(tab_ui, key, type_value, items, locations):
    # Determine if Type and TypeText should be shown (based on tab name)
    if key in items or key in locations:
        tab_ui.Type.setVisible(False)
        tab_ui.TypeText.setVisible(False)
    else:
        tab_ui.Type.setVisible(True)
        tab_ui.TypeText.setVisible(True)
        if type_value == "Custom":
            tab_ui.FilterInclude.setVisible(False)
            tab_ui.FilterExclude.setVisible(False)
            tab_ui.FilterIncludeText.setVisible(False)
            tab_ui.FilterExcludeText.setVisible(False)
        else:
            tab_ui.FilterInclude.setVisible(True)
            tab_ui.FilterExclude.setVisible(True)
            tab_ui.FilterIncludeText.setVisible(True)
            tab_ui.FilterExcludeText.setVisible(True)

def filter_include_exclude_lists(tab_ui, game_name, type_value):
    search_text = tab_ui.SearchInputInclude.text().strip().lower()
    filter_include_group = tab_ui.FilterInclude.currentText()
    filter_exclude_group = tab_ui.FilterExclude.currentText()

    include_model = tab_ui.IncludeList.model()
    exclude_model = tab_ui.ExcludeList.model()
    if include_model is None or exclude_model is None:
        return  # Models not initialized yet

    # Get all items from models
    all_include_items = include_model.stringList()
    all_exclude_items = exclude_model.stringList()

    # Load group data if needed
    group_items_include = set()
    group_items_exclude = set()

    if type_value == "Item":
        data_type = "item_groups"
    elif type_value == "Location":
        data_type = "location_groups"
    else:
        data_type = None  # Custom tabs do not filter by group

    if data_type:
        # Load include group (skip defaults)
        if filter_include_group not in {"Everything", "Everywhere", "Nothing", "Nowhere"}:
            group_items_include = set(get_extracted_data(game_name, data_type, filter_include_group))

        # Load exclude group (skip defaults)
        if filter_exclude_group not in {"Everything", "Everywhere", "Nothing", "Nowhere"}:
            group_items_exclude = set(get_extracted_data(game_name, data_type, filter_exclude_group))

    # Filter IncludeList
    for row in range(include_model.rowCount()):
        item_text = include_model.data(include_model.index(row, 0)).strip()
        match_search = (not search_text) or (search_text in item_text.lower())
        match_group = (not group_items_include) or (item_text in group_items_include)
        match_exclude = (not group_items_exclude) or (item_text not in group_items_exclude)

        visible = match_search and match_group and match_exclude
        tab_ui.IncludeList.setRowHidden(row, not visible)

    # Filter ExcludeList (same logic)
    for row in range(exclude_model.rowCount()):
        item_text = exclude_model.data(exclude_model.index(row, 0)).strip()
        match_search = (not search_text) or (search_text in item_text.lower())
        match_group = (not group_items_include) or (item_text in group_items_include)
        match_exclude = (not group_items_exclude) or (item_text not in group_items_exclude)

        visible = match_search and match_group and match_exclude
        tab_ui.ExcludeList.setRowHidden(row, not visible)