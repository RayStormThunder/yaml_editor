from PySide6.QtWidgets import QWidget, QSpacerItem, QSizePolicy, QLabel, QComboBox, QLineEdit, QSpinBox, QVBoxLayout
from PySide6.QtCore import Qt, QObject, QEvent
from ui_row import Ui_BasicRow
from ui_weighted_row import Ui_WeightedRow
from ui_weighted_sub_row import Ui_SepecificSetting
from description import set_description_text
from spacer_utils import move_spacer
from stored_gui import get_global_setting, global_settings

import config  # Import the debug flag

class NoScrollComboBoxFilter(QObject):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Wheel:
            return True  # Block the wheel event
        return super().eventFilter(obj, event)

def clear_all_rows(main_window):
    scroll_area = main_window.ui.ScrollMain
    scroll_content = scroll_area.widget()
    scroll_layout = scroll_content.layout()

    while scroll_layout.count():
        child = scroll_layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()

    # Reset row_data and template_items
    main_window.row_data = []

def add_both_rows(main_window, name, items, description="", starting_item="", original_selected=None, base_yaml_selected=None):
    add_normal_row(main_window, name, items, description, starting_item, original_selected, base_yaml_selected)
    add_weighted_row(main_window, name, items, description, starting_item)

def add_normal_row(main_window, name: str, items: dict, description: str = "", starting_item: str = "", original_selected=None, base_yaml_selected=None):
    row_widget = QWidget()
    row_widget.row_type = "normal"
    row_ui = Ui_BasicRow()
    row_ui.setupUi(row_widget)

    if config.debug_flag:
        print(f"[add_rows] [normal] base_items: {items}")
        print(f"[add_rows] [normal] starting_item: {starting_item}")

    row_ui.SettingLabel.setText(name)

    item_list = [str(k) for k in items.keys()]
    if starting_item and starting_item not in item_list:
        item_list.insert(0, starting_item)

    row_ui.SettingSimpleCombo.addItems(item_list)

    if starting_item:
        index = item_list.index(starting_item)
        row_ui.SettingSimpleCombo.setCurrentIndex(index)

    row_ui.SettingSimpleCombo._no_scroll_filter = NoScrollComboBoxFilter()
    row_ui.SettingSimpleCombo.installEventFilter(row_ui.SettingSimpleCombo._no_scroll_filter)

    scroll_area = main_window.ui.ScrollMain
    scroll_content = scroll_area.widget()
    scroll_layout = scroll_content.layout()

    move_spacer(scroll_layout)
    scroll_layout.insertWidget(scroll_layout.count() - 1, row_widget)

    if not hasattr(main_window, "row_data"):
        main_window.row_data = []

    main_window.row_data.append({
        "name": name,
        "description": description,
        "selected_item": starting_item,
        "program_start_item": starting_item,
        "original_selected": original_selected or "",
        "base_yaml_selected": base_yaml_selected or ""
    })


    row_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

    def on_enter(event, desc=description):
        set_description_text(main_window, desc)

    row_widget.enterEvent = on_enter

    template_values = main_window.template_items.get(name, [])

    def validate_custom_background():
        current_value = row_ui.SettingSimpleCombo.currentText()
        original_value = original_selected or ""
        starting_value = starting_item or ""
        template_value = base_yaml_selected or ""
        
        apply_normal_custom_style(
            row_ui.SettingSimpleCombo,
            current_value=current_value,
            starting_value=starting_value,
            template_values=template_values,
            template_value=template_value
        )

    row_index = len(main_window.row_data) - 1

    def on_combo_change(index, row_index=row_index):
        selected_item = row_ui.SettingSimpleCombo.itemText(index)
        normal_changed(main_window, row_index, selected_item)
        validate_custom_background()
        if config.debug_flag:
            print("[DEBUG] Updated row_data:", main_window.row_data)

    row_ui.SettingSimpleCombo.currentIndexChanged.connect(on_combo_change)

    def on_combo_edit_finished(row_index=row_index):
        selected_item = row_ui.SettingSimpleCombo.currentText()
        normal_changed(main_window, row_index, selected_item)
        validate_custom_background()
        if config.debug_flag:
            print("[DEBUG] Applied edited combo box text:", selected_item)

    combo_editor = row_ui.SettingSimpleCombo.lineEdit()
    if combo_editor:
        combo_editor.editingFinished.connect(on_combo_edit_finished)

    validate_custom_background()

def normal_changed(main_window, row_index, selected_item):
    main_window.row_data[row_index]["selected_item"] = selected_item
    if config.debug_flag:
        print("[DEBUG] Updated row_data:", main_window.row_data)

    current_name = main_window.row_data[row_index]["name"]

    for i in range(main_window.ui.ScrollMain.widget().layout().count()):
        other_widget = main_window.ui.ScrollMain.widget().layout().itemAt(i).widget()
        if getattr(other_widget, "row_type", None) == "weighted":
            name_label = other_widget.findChild(QLabel, "Name")
            if name_label and name_label.text() == current_name:
                sub_widgets = [other_widget.sub_row_holder.itemAt(i).widget() for i in range(other_widget.sub_row_holder.count())]

                # Check if the selected item exists in weighted sub-rows
                found = False
                for sub in sub_widgets:
                    name_field = sub.findChild(QLineEdit, "SpecificSettingName")
                    if name_field and name_field.text() == selected_item:
                        found = True
                        break

                if not found:
                    # Add new weighted sub-row for new item
                    add_weighted_sub_row(main_window, other_widget, selected_item, 50)
                    # Set others to 0
                    for sub in sub_widgets:
                        spin = sub.findChild(QSpinBox, "SpecificSettingNumber")
                        if spin:
                            spin.setValue(0)
                    weighted_changed(main_window, other_widget)  # Sync after adding
                    return  # Done, no need to proceed

                # Continue with existing behavior if it already exists
                spin_values = []
                for sub in sub_widgets:
                    spin = sub.findChild(QSpinBox, "SpecificSettingNumber")
                    if spin:
                        if config.debug_flag:
                            print(spin.value())
                        spin_values.append(spin.value())
                nonzero = [v for v in spin_values if v > 0]
                if len(nonzero) == 1 and 50 in nonzero:
                    for sub in sub_widgets:
                        name_field = sub.findChild(QLineEdit, "SpecificSettingName")
                        spin = sub.findChild(QSpinBox, "SpecificSettingNumber")
                        if spin and name_field:
                            if name_field.text() == selected_item:
                                spin.setValue(50)
                            else:
                                spin.setValue(0)
                    weighted_changed(main_window, other_widget)  # Sync


def apply_normal_custom_style(widget, current_value, starting_value, template_values, template_value):
    color = ""
    red_enabled = get_global_setting("RedState", False)
    green_enabled = get_global_setting("GreenState", False)
    blue_enabled = get_global_setting("BlueState", False)

    if current_value not in template_values and red_enabled:
        color = "#5c4e1e"  # Red - not in template
    elif current_value != starting_value and green_enabled:
        color = "#1e5c2a"  # Green - changed
    elif template_value is not None and current_value != template_value and blue_enabled:
        color = "#1e2e5c"  # Blue - default mismatch

    if color:
        widget.setStyleSheet(f"""
            QWidget {{
                background-color: {color};
                color: white;
            }}
            QLineEdit, QSpinBox {{
                font-size: 12pt;
            }}
        """)
    else:
        widget.setStyleSheet("""
            QLineEdit, QSpinBox {
                font-size: 12pt;
            }
        """)


def apply_weighted_custom_style(widget, current_value, original_value, template_values, template_value, row_name, item_name):
    color = ""
    green_enabled = get_global_setting("GreenState", False)
    red_enabled = get_global_setting("RedState", False)
    blue_enabled = get_global_setting("BlueState", False)

    if item_name not in template_values and red_enabled:
        color = "#5c4e1e"  # Red - not in template
    elif current_value != original_value and green_enabled:
        color = "#1e5c2a"  # Green - changed
    elif template_value is not None and current_value != template_value and blue_enabled:
        color = "#1e2e5c"  # Blue - default mismatch


    if color:
        widget.setStyleSheet(f"""
            QWidget {{
                background-color: {color};
                color: white;
            }}
            QLineEdit, QSpinBox {{
                font-size: 12pt;
            }}
        """)
    else:
        widget.setStyleSheet("""
            QLineEdit, QSpinBox {
                font-size: 12pt;
            }
        """)


def add_weighted_row(main_window, name: str, items: dict, description: str = "", starting_item: str = ""):
    row_widget = QWidget()
    row_widget.row_type = "weighted"
    row_ui = Ui_WeightedRow()
    row_ui.setupUi(row_widget)
    original_weights = {}  # ← Track initial values

    if config.debug_flag:
        print(f"[add_rows] [weighted] base_items: {items}")
        print(f"[add_rows] [weighted] starting_item: {starting_item}")
        print()

    row_ui.Name.setText(name)
    template_dict = main_window.template_items_full.get(name, {})
    template_values = list(template_dict.keys())

    for item_name, value in items.items():
        original_weights[item_name] = int(value)

        sub_widget = QWidget()
        sub_ui = Ui_SepecificSetting()
        sub_ui.setupUi(sub_widget)

        sub_ui.SpecificSettingName.setText(str(item_name))
        sub_ui.SpecificSettingNumber.setValue(int(value))

        def make_value_changed_handler(sub_widget, sub_ui, item_name):
            def on_value_changed():
                current_value = sub_ui.SpecificSettingNumber.value()
                original_value = original_weights.get(item_name, 0)
                template_value = template_dict.get(item_name)

                apply_weighted_custom_style(
                    sub_widget,
                    current_value=current_value,
                    original_value=original_value,
                    template_values=template_values,
                    template_value=template_value,
                    row_name=name,
                    item_name=item_name
                )
                weighted_changed(main_window, row_widget)
            return on_value_changed

        # Connect the wrapped handler
        sub_ui.SpecificSettingNumber.valueChanged.connect(make_value_changed_handler(sub_widget, sub_ui, item_name))

        # Apply initial style
        apply_weighted_custom_style(
            sub_widget,
            current_value=value,
            original_value=original_weights.get(item_name, 0),
            template_values=template_values,
            template_value=template_dict.get(item_name),
            row_name=name,
            item_name=item_name
        )

        row_ui.SubRowHolder.addWidget(sub_widget)

    row_widget.sub_row_holder = row_ui.SubRowHolder
    row_widget.original_weights = original_weights  # Store for future use

    scroll_area = main_window.ui.ScrollMain
    scroll_content = scroll_area.widget()
    scroll_layout = scroll_content.layout()

    move_spacer(scroll_layout)
    scroll_layout.insertWidget(scroll_layout.count() - 1, row_widget)

    if not hasattr(main_window, "row_data"):
        main_window.row_data = []

    main_window.row_data.append({
        "name": name,
        "description": description,
        "selected_item": starting_item,
        "weights": items.copy()
    })

    row_ui.AddRow.clicked.connect(
        lambda checked=False, row_widget=row_widget: add_weighted_sub_row(main_window, row_widget)
    )

    row_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

    def on_enter(event, desc=description):
        set_description_text(main_window, desc)

    row_widget.enterEvent = on_enter

def weighted_changed(main_window, row_widget):
    name_label = row_widget.findChild(QLabel, "Name")
    if not name_label:
        return

    current_name = name_label.text()

    sub_widgets = [row_widget.sub_row_holder.itemAt(i).widget() for i in range(row_widget.sub_row_holder.count())]
    highest_value = -1
    highest_item = None
    for sub in sub_widgets:
        name_field = sub.findChild(QLineEdit, "SpecificSettingName")
        spin = sub.findChild(QSpinBox, "SpecificSettingNumber")
        if spin and name_field:
            v = spin.value()
            if v > highest_value:
                highest_value = v
                highest_item = name_field.text()

    for i in range(main_window.ui.ScrollMain.widget().layout().count()):
        other_widget = main_window.ui.ScrollMain.widget().layout().itemAt(i).widget()
        if getattr(other_widget, "row_type", None) == "normal":
            normal_name_label = other_widget.findChild(QLabel, "SettingLabel")
            if normal_name_label and normal_name_label.text() == current_name:
                combo = other_widget.findChild(QComboBox, "SettingSimpleCombo")
                if combo.findText(highest_item) == -1:
                    # Item doesn't exist, add it
                    combo.addItem(highest_item)
                idx = combo.findText(highest_item)
                if idx >= 0:
                    combo.setCurrentIndex(idx)
                break  # Found matching normal row

def add_weighted_sub_row(main_window, weighted_row_widget, name_text="", number_value=0):
    sub_widget = QWidget()
    sub_ui = Ui_SepecificSetting()
    sub_ui.setupUi(sub_widget)

    sub_ui.SpecificSettingName.setText(str(name_text))
    sub_ui.SpecificSettingNumber.setValue(int(number_value))

    # Immediately apply color styling after setting up
    item_name = name_text
    current_value = number_value

    original_weights = getattr(weighted_row_widget, "original_weights", {})
    template_dict = main_window.template_items_full.get(weighted_row_widget.findChild(QLabel, "Name").text(), {})
    template_values = list(template_dict.keys())
    template_value = template_dict.get(item_name)
    original_value = original_weights.get(item_name, 0)

    apply_weighted_custom_style(
        sub_widget,
        current_value=current_value,
        original_value=original_value,
        template_values=template_values,
        template_value=template_value,
        row_name=weighted_row_widget.findChild(QLabel, "Name").text(),
        item_name=item_name
    )

    # Set up live updating logic
    def on_value_changed():
        current_value = sub_ui.SpecificSettingNumber.value()
        apply_weighted_custom_style(
            sub_widget,
            current_value=current_value,
            original_value=original_weights.get(item_name, 0),
            template_values=template_values,
            template_value=template_value,
            row_name=weighted_row_widget.findChild(QLabel, "Name").text(),
            item_name=item_name
        )
        weighted_changed(main_window, weighted_row_widget)

    sub_ui.SpecificSettingNumber.valueChanged.connect(on_value_changed)

    weighted_row_widget.sub_row_holder.addWidget(sub_widget)

def filter_rows(main_window, text):
    weighted_enabled = main_window.ui.WeightedSettingsEnabled.isChecked()

    for i in range(main_window.ui.ScrollMain.widget().layout().count()):
        row_widget = main_window.ui.ScrollMain.widget().layout().itemAt(i).widget()
        if row_widget is None:
            continue  # Skip spacers or empty items

        # Skip rows that are not visible due to weighted toggle
        if hasattr(row_widget, "row_type"):
            if (row_widget.row_type == "weighted" and not weighted_enabled) or \
               (row_widget.row_type == "normal" and weighted_enabled):
                row_widget.setVisible(False)
                continue  # Don't search hidden types

        # Search normally if row type matches weighted toggle
        matches = False
        for child in row_widget.findChildren(QLabel):
            if text.lower() in child.text().lower():
                matches = True
                break

        if not matches:
            for child in row_widget.findChildren(QComboBox):
                for i in range(child.count()):
                    if text.lower() in child.itemText(i).lower():
                        matches = True
                        break
                if matches:
                    break

        if not matches:
            for child in row_widget.findChildren(QLineEdit):
                if text.lower() in child.text().lower():
                    matches = True
                    break

        row_widget.setVisible(matches)

def setup_row_style_signal(scroll_area, template_items, template_items_full, row_data):
    def refresh_row_styles_from_settings():
        for i in range(scroll_area.widget().layout().count()):
            row_widget = scroll_area.widget().layout().itemAt(i).widget()
            if not row_widget:
                continue

            row_type = getattr(row_widget, "row_type", None)

            if row_type == "normal":
                name_label = row_widget.findChild(QLabel, "SettingLabel")
                combo = row_widget.findChild(QComboBox, "SettingSimpleCombo")
                if not name_label or not combo:
                    continue

                row_name = name_label.text()
                current_value = combo.currentText()

                template_values = template_items.get(row_name, [])
                original_selected = ""
                base_yaml_selected = ""

                for entry in row_data:
                    if entry["name"] == row_name:
                        original_selected = entry.get("original_selected") or ""
                        starting_selected = entry.get("program_start_item") or ""
                        base_yaml_selected = entry.get("base_yaml_selected") or ""
                        break

                apply_normal_custom_style(
                    combo,
                    current_value=current_value,
                    starting_value=starting_selected,
                    template_values=template_values,
                    template_value=base_yaml_selected
                )

            elif row_type == "weighted":
                name_label = row_widget.findChild(QLabel, "Name")
                if not name_label:
                    continue

                row_name = name_label.text()
                template_dict = template_items_full.get(row_name, {})
                template_values = list(template_dict.keys())
                original_weights = getattr(row_widget, "original_weights", {})

                sub_row_holder = row_widget.findChild(QVBoxLayout, "SubRowHolder")
                if not sub_row_holder:
                    continue

                for j in range(sub_row_holder.count()):
                    sub_widget = sub_row_holder.itemAt(j).widget()
                    if not sub_widget:
                        continue

                    name_field = sub_widget.findChild(QLineEdit, "SpecificSettingName")
                    spin = sub_widget.findChild(QSpinBox, "SpecificSettingNumber")
                    if not name_field or not spin:
                        continue

                    item_name = name_field.text()
                    current_value = spin.value()
                    original_value = original_weights.get(item_name, 0)
                    template_value = template_dict.get(item_name)

                    apply_weighted_custom_style(
                        sub_widget,
                        current_value=current_value,
                        original_value=original_value,
                        template_values=template_values,
                        template_value=template_value,
                        row_name=row_name,
                        item_name=item_name
                    )

    # Connect once per-instance of tab/view
    global_settings.changed.connect(
        lambda key, value: refresh_row_styles_from_settings()
        if key in ("RedState", "GreenState", "BlueState") else None
    )
