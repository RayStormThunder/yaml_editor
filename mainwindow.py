# This Python file uses the following encoding: utf-8
import sys
import os
import yaml
import shutil

#Pyside
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PySide6.QtCore import QTimer

#python imports
import config
from add_rows import add_both_rows, filter_rows
from description import set_description_text, show_description_text
from game_and_slot_setup import refresh_games_and_slots
from stored_gui import set_yaml_setting, get_yaml_setting, set_global_setting, get_global_setting
from paths import get_base_folder, get_exe_folder
from datapackage_conversion import extract_datapackages

config.debug_flag = False  # Enable debug logging globally

from ui_main import Ui_MainWindow
from ui_row import Ui_BasicRow
from ui_weighted_row import Ui_WeightedRow
from ui_weighted_sub_row import Ui_SepecificSetting

def extract_datapackages_and_create_yaml_folder():
        exe_folder = get_exe_folder()
        base_folder = get_base_folder()

        # Extract Datapackages folder
        source_path = os.path.join(base_folder, "Datapackages")
        dest_path = os.path.join(exe_folder, "Datapackages")

        if not os.path.exists(dest_path):
                try:
                        shutil.copytree(source_path, dest_path)
                        print(f"[INFO] Extracted Datapackages to {dest_path}")
                except Exception as e:
                        print(f"[ERROR] Failed to extract Datapackages: {e}")
        else:
                print(f"[INFO] Datapackages already exists at {dest_path}")

        # Create YAMLS folder if it doesn't exist
        yamls_path = os.path.join(exe_folder, "YAMLS")
        if not os.path.exists(yamls_path):
                try:
                        os.makedirs(yamls_path)
                        print(f"[INFO] Created YAMLS folder at {yamls_path}")
                except Exception as e:
                        print(f"[ERROR] Failed to create YAMLS folder: {e}")
        else:
                print(f"[INFO] YAMLS folder already exists at {yamls_path}")

class MainWindow(QMainWindow):
        def __init__(self, parent=None):
                super().__init__(parent)
                self.ui = Ui_MainWindow()
                self.ui.setupUi(self)
                self.ui.SearchField.textChanged.connect(lambda text: filter_rows(self, text))
                self.setWindowTitle("YAML Editor 2.0.0")

                self.setStyleSheet("""
                        QScrollArea {
                                background-color: #2c2c2c;
                                border: 1px solid #444;
                        }

                        QTextEdit {
                                background-color: #1e1e1e;
                                color: #dcdcdc;
                                border: 1px solid #444;
                        }

                        QComboBox, QLineEdit, QListView {
                                background-color: #2c2c2c;
                                color: #dcdcdc;
                                border: 1px solid #444;
                        }

                        QWidget {
                                color: #dcdcdc;
                        }
                """)

                scroll_content = self.ui.ScrollMain.widget()
                scroll_layout = QVBoxLayout()
                scroll_content.setLayout(scroll_layout)

                self.ui.ScrollSlot.widget().setLayout(QVBoxLayout())
                self.ui.ScrollGame.widget().setLayout(QVBoxLayout())

                self.selected_game = None
                self.selected_slot = None
                self.selected_game = get_global_setting("Last Selected Game", None)
                self.selected_slot = get_global_setting("Last Selected Slot", None)


                # Start timer to auto-refresh every 1000 ms
                self.refresh_timer = QTimer(self)
                self.refresh_timer.timeout.connect(self.refresh_game_and_slot_lists)
                self.refresh_timer.start(1000)  # 1 second

                # Initial load
                self.refresh_game_and_slot_lists()

                self.ui.LoadYamlButton.clicked.connect(self.on_load_yaml_with_refresh)
                self.ui.WeightedSettingsEnabled.stateChanged.connect(self.on_weighted_toggle)

                # Load global setting for HideDescriptionTextEnabled
                hide_enabled = get_global_setting("Hide Setting Description", False)
                self.ui.HideDescriptionTextEnabled.setChecked(hide_enabled)
                self.ui.DescriptionText.setVisible(not hide_enabled)
                self.ui.HideDescriptionTextEnabled.stateChanged.connect(self.on_hide_description_toggle)
                self.ui.SaveYamlButton.clicked.connect(self.on_save_yaml_clicked)

        def on_save_yaml_clicked(self):
                from save_yaml import save_yaml
                save_yaml(self)

        def on_hide_description_toggle(self):
                hide_enabled = self.ui.HideDescriptionTextEnabled.isChecked()
                self.ui.DescriptionText.setVisible(not hide_enabled)

                # Save global setting
                set_global_setting("Hide Setting Description", hide_enabled)

        def on_load_yaml_with_refresh(self):
                self.refresh_game_and_slot_lists(True)
                self.on_load_yaml_clicked()

        def on_weighted_toggle(self):
                weighted_enabled = self.ui.WeightedSettingsEnabled.isChecked()
                self.toggle_row_visibility(weighted_enabled)
                filter_rows(self, self.ui.SearchField.text())

                # Save YAML-specific setting only if YAML loaded
                if hasattr(self, "current_yaml_path") and self.current_yaml_path:
                        from os.path import basename
                        yaml_name = basename(self.current_yaml_path)
                        set_yaml_setting(yaml_name, "Enter Weighted Option Mode", weighted_enabled)

        def refresh_game_and_slot_lists(self, override=False):
                from game_and_slot_setup import refresh_games_and_slots

                self.selected_game, self.selected_slot = refresh_games_and_slots(
                        self,
                        self.selected_game,
                        self.selected_slot,
                        override
                )

                if self.selected_game:
                        set_global_setting("Last Selected Game", self.selected_game)
                if self.selected_slot:
                        set_global_setting("Last Selected Slot", self.selected_slot)


        def on_load_yaml_clicked(self):
            if hasattr(self, "current_yaml_path") and self.current_yaml_path:
                from load_yaml_data import load_yaml_UI
                selected_yaml_path = self.current_yaml_path

                with open(selected_yaml_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if isinstance(data, dict) and "game" in data:
                        base_game = str(data["game"])
                        yaml_base_folder = os.path.join(get_exe_folder(), "YAMLS")
                        base_yaml_path = os.path.join(yaml_base_folder, f"{base_game}.yaml")

                        print("[INFO] Selected Slot YAML:", selected_yaml_path)
                        if config.debug_flag:
                                print("[INFO] Base Game YAML:", base_yaml_path)

                        if os.path.exists(base_yaml_path):
                            # WeightedSettingsEnabled toggle
                            load_yaml_UI(self, base_yaml_path, selected_yaml_path, base_game)
                            filter_rows(self, self.ui.SearchField.text())
                        else:
                            print(f"[ERROR] Base YAML for game '{base_game}' not found: {base_yaml_path}")

                        from os.path import basename
                        yaml_name = basename(selected_yaml_path)
                        weighted_enabled = get_yaml_setting(yaml_name, "Enter Weighted Option Mode", False)
                        self.ui.WeightedSettingsEnabled.setChecked(weighted_enabled)
                    else:
                        print(f"[ERROR] 'game' field missing in selected YAML: {selected_yaml_path}")
            else:
                print("[WARNING] No YAML file currently selected.")

        def toggle_row_visibility(self, weighted_enabled):
            for i in range(self.ui.ScrollMain.widget().layout().count()):
                row_widget = self.ui.ScrollMain.widget().layout().itemAt(i).widget()
                if row_widget is None:
                    continue  # Skip spacers or empty items

                if hasattr(row_widget, "row_type"):  # We'll set this in your row creation functions
                    if row_widget.row_type == "weighted":
                        row_widget.setVisible(weighted_enabled)
                    elif row_widget.row_type == "normal":
                        row_widget.setVisible(not weighted_enabled)

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
            extract_datapackages_and_create_yaml_folder()
    extract_datapackages()
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
