from PySide6.QtWidgets import QWidget, QSpacerItem, QSizePolicy, QLabel, QComboBox, QLineEdit, QSpinBox, QVBoxLayout
from PySide6.QtCore import Qt, QObject, QEvent
from ui_row import Ui_BasicRow
from ui_weighted_row import Ui_WeightedRow
from ui_weighted_sub_row import Ui_SepecificSetting
from description import set_description_text
from spacer_utils import move_spacer

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

    # Reset row_data list
    main_window.row_data = []

def add_both_rows(main_window, name: str, items: dict, description: str = "", starting_item: str = ""):
    add_normal_row(main_window, name, items, description, starting_item)
    add_weighted_row(main_window, name, items, description, starting_item)

def add_normal_row(main_window, name: str, items: dict, description: str = "", starting_item: str = ""):
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
        "selected_item": starting_item
    })

    row_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

    def on_enter(event, desc=description):
        set_description_text(main_window, desc)

    row_widget.enterEvent = on_enter

    row_index = len(main_window.row_data) - 1

    def on_combo_change(index, row_index=row_index):
        selected_item = row_ui.SettingSimpleCombo.itemText(index)
        normal_changed(main_window, row_index, selected_item)
        if config.debug_flag:
            print("[DEBUG] Updated row_data:", main_window.row_data)

    row_ui.SettingSimpleCombo.currentIndexChanged.connect(on_combo_change)

    def on_combo_edit_finished(row_index):
        selected_item = row_ui.SettingSimpleCombo.currentText()
        normal_changed(main_window, row_index, selected_item)
        if config.debug_flag:
            print("[DEBUG] Applied edited combo box text:", selected_item)

    combo_editor = row_ui.SettingSimpleCombo.lineEdit()
    if combo_editor:
        combo_editor.editingFinished.connect(
            lambda row_index=row_index: on_combo_edit_finished(row_index)
        )


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

def add_weighted_row(main_window, name: str, items: dict, description: str = "", starting_item: str = ""):
    row_widget = QWidget()
    row_widget.row_type = "weighted"
    row_ui = Ui_WeightedRow()
    row_ui.setupUi(row_widget)
    if config.debug_flag:
        print(f"[add_rows] [weighted] base_items: {items}")
        print(f"[add_rows] [weighted] starting_item: {starting_item}")
        print()

    row_ui.Name.setText(name)

    for item_name, value in items.items():
        sub_widget = QWidget()
        sub_ui = Ui_SepecificSetting()
        sub_ui.setupUi(sub_widget)

        sub_ui.SpecificSettingName.setText(str(item_name))
        sub_ui.SpecificSettingNumber.setValue(int(value))
        sub_ui.SpecificSettingNumber.valueChanged.connect(
            lambda _, row_widget=row_widget: weighted_changed(main_window, row_widget)
        )

        row_ui.SubRowHolder.addWidget(sub_widget)
    row_widget.sub_row_holder = row_ui.SubRowHolder

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
    sub_ui.SpecificSettingNumber.valueChanged.connect(
        lambda _, row_widget=weighted_row_widget: weighted_changed(main_window, row_widget)
    )

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
