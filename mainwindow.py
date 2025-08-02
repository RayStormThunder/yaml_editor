# This Python file uses the following encoding: utf-8
import sys
import os
import yaml
import shutil
import platform
import winreg

#Pyside
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPalette, QColor, QPixmap

#python imports
import config
from version import VERSION
from add_rows import add_both_rows, filter_rows
from description import set_description_text, show_description_text
from game_and_slot_setup import refresh_games_and_slots
from stored_gui import set_yaml_setting, get_yaml_setting, set_global_setting, get_global_setting
from paths import get_base_folder, get_exe_folder
from datapackage_conversion import extract_datapackages, update_datapackage
from path_fixer import sanitize_path_component

config.debug_flag = False  # Enable debug logging globally

from ui_main import Ui_MainWindow
from ui_row import Ui_BasicRow
from ui_weighted_row import Ui_WeightedRow
from ui_weighted_sub_row import Ui_SepecificSetting

def is_dark_mode():
        try:
                reg_key = winreg.OpenKey(
                        winreg.HKEY_CURRENT_USER,
                        r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
                )
                value, _ = winreg.QueryValueEx(reg_key, "AppsUseLightTheme")
                return value == 0  # 0 = dark mode, 1 = light mode
        except Exception:
                return False  # Assume light mode if detection fails

def is_windows_11():
        version = platform.version().split('.')
        try:
                build = int(version[2])
                return build >= 22000  # Windows 11 builds start from 22000
        except (IndexError, ValueError):
                return False

def apply_dark_theme(app):
        app.setStyleSheet("""
                /* Background & Text Colors Only */
                QWidget {
                        background-color: #1e1e1e;
                        color: #d4d4d4;
                }

                QFrame {
                        background-color: #2c2c2c;
                }

                QLineEdit, QPlainTextEdit, QTextEdit {
                        background-color: #2d2d2d;
                        color: #d4d4d4;
                }

                QComboBox {
                        background-color: #2d2d2d;
                        color: #d4d4d4;
                }

                QPushButton {
                        background-color: #2d2d2d;
                        color: #d4d4d4;
                }

                QCheckBox, QRadioButton {
                        color: #d4d4d4;
                }

                QRadioButton::indicator {
                        width: 16px;
                        height: 16px;
                        border: 2px solid #d4d4d4;
                        border-radius: 8px;
                        background-color: #2d2d2d;
                }

                QScrollArea {
                        background-color: #1e1e1e;
                }

                QScrollArea > QWidget > QWidget {
                        background-color: #1e1e1e;
                }

                QScrollArea QWidget {
                        background-color: #1e1e1e;
                }

                QRadioButton::indicator:checked {
                        background-color: #d4d4d4;
                }

                QTabWidget::pane {
                        background-color: #2c2c2c;
                }

                QCheckBox::indicator {
                        width: 16px;
                        height: 16px;
                        border: 2px solid #d4d4d4;
                        background-color: #2d2d2d;
                }

                QCheckBox::indicator:checked {
                        background-color: #d4d4d4;
                }

                QTabWidget QWidget {
                        background-color: #2c2c2c;
                }

                QTabBar::tab {
                        background-color: #1e1e1e;
                        color: #d4d4d4;
                        border: 2px solid #2d2d2d;
                        border-radius: 6px;
                        padding: 4px;
                }

                QTabBar::tab:selected,
                QTabBar::tab:hover {
                        background-color: #2d2d2d;
                        border: 2px solid #2d2d2d;
                        border-radius: 6px;
                }

                QListWidget, QListView, QTreeView {
                        background-color: #2d2d2d;
                        color: #d4d4d4;
                }

                /* Scrollbar Styling */
                QScrollBar:vertical, QScrollBar:horizontal {
                        background: #2d2d2d;
                        width: 12px;
                        height: 12px;
                        margin: 0px;
                        border: none;
                }

                QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                        background: #888888;
                        border-radius: 6px;
                        min-height: 20px;
                        min-width: 20px;
                }

                QScrollBar::handle:hover {
                        background: #aaaaaa;
                }

                QScrollBar::handle:pressed {
                        background: #d4d4d4;
                }

                QScrollBar::add-line, QScrollBar::sub-line {
                        background: none;
                        border: none;
                        width: 0px;
                        height: 0px;
                }

                QScrollBar::add-page, QScrollBar::sub-page {
                        background: none;
                }
        """)


def create_datapackages_and_yaml_folders():
        exe_folder = get_exe_folder()

        # Create Datapackages folder
        datapackages_path = os.path.join(exe_folder, "Datapackages")
        if not os.path.exists(datapackages_path):
                try:
                        os.makedirs(datapackages_path)
                        print(f"[mainwindow] [INFO] Created Datapackages folder at {datapackages_path}")
                except Exception as e:
                        print(f"[mainwindow] [ERROR] Failed to create Datapackages folder: {e}")
        else:
                print(f"[mainwindow] [INFO] Datapackages folder already exists at {datapackages_path}")

        # Create YAMLS folder
        yamls_path = os.path.join(exe_folder, "YAMLS")
        if not os.path.exists(yamls_path):
                try:
                        os.makedirs(yamls_path)
                        print(f"[mainwindow] [INFO] Created YAMLS folder at {yamls_path}")
                except Exception as e:
                        print(f"[mainwindow] [ERROR] Failed to create YAMLS folder: {e}")
        else:
                print(f"[mainwindow] [INFO] YAMLS folder already exists at {yamls_path}")

class MainWindow(QMainWindow):
        def __init__(self, parent=None):
                super().__init__(parent)
                global VERSION
                self.ui = Ui_MainWindow()
                self.ui.setupUi(self)
                self.ui.SearchField.textChanged.connect(lambda text: filter_rows(self, text))
                self.setWindowTitle(f"YAML Editor {VERSION}")

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

                # Ensure global color states are set to True by default if missing
                for key in ("RedState", "BlueState", "GreenState"):
                        value = get_global_setting(key)
                        if value is None:
                                set_global_setting(key, True)  # Set default if not present

                self.ui.RedState.setChecked(get_global_setting("RedState"))
                self.ui.BlueState.setChecked(get_global_setting("BlueState"))
                self.ui.GreenState.setChecked(get_global_setting("GreenState"))

                self.ui.SaveYamlButton.clicked.connect(self.on_save_yaml_clicked)

                update_datapackage()

                # Connect signals to update SaveYamlButton text
                self.ui.YAMLLineEdit.textChanged.connect(self.update_save_yaml_button_text)
                self.ui.GameLineEdit.textChanged.connect(self.update_save_yaml_button_text)

                # Initial set of the button text
                self.update_save_yaml_button_text()

                # Server Connection
                self.row_check_timer = QTimer(self)
                self.row_check_timer.timeout.connect(self.check_if_rows_exist_and_set_text)
                self.row_check_timer.start(100)

                self.ui.RedState.stateChanged.connect(self.on_red_state_toggle)
                self.ui.BlueState.stateChanged.connect(self.on_blue_state_toggle)
                self.ui.GreenState.stateChanged.connect(self.on_green_state_toggle)

                self.easter_egg_scene = QGraphicsScene()
                self.ui.EasterEgg.setScene(self.easter_egg_scene)

                self.easter_egg_images = []
                self.easter_egg_image_size = (24, 24)
                images_dir = os.path.join(get_exe_folder(), "images")
                for file in os.listdir(images_dir):
                        if file.lower().endswith((".png", ".gif")):
                                self.easter_egg_images.append(os.path.join(images_dir, file))

                self.easter_egg_index = 0

                def update_easter_egg_image():
                        if not self.easter_egg_images:
                                return
                        self.easter_egg_scene.clear()
                        image_path = self.easter_egg_images[self.easter_egg_index]
                        pixmap = QPixmap(image_path).scaled(
                            self.easter_egg_image_size[0],
                            self.easter_egg_image_size[1],
                            Qt.KeepAspectRatio,
                            Qt.SmoothTransformation
                        )

                        item = QGraphicsPixmapItem(pixmap)
                        self.easter_egg_scene.addItem(item)
                        self.easter_egg_index = (self.easter_egg_index + 1) % len(self.easter_egg_images)

                self.easter_egg_timer = QTimer(self)
                self.easter_egg_timer.timeout.connect(update_easter_egg_image)
                self.easter_egg_timer.start(2000)  # Change image every 2 seconds

                update_easter_egg_image()  # Show first image immediately
                self.ui.EasterEgg.setVisible(False)  # Hide initially
                self.ui.YAMLLineEdit.textChanged.connect(self.check_easter_egg_visibility)


        def check_easter_egg_visibility(self, text: str):
                if text.strip().lower() == "dango":
                        self.ui.EasterEgg.setVisible(True)
                else:
                        self.ui.EasterEgg.setVisible(False)

        def on_red_state_toggle(self):
                set_global_setting("RedState", self.ui.RedState.isChecked())

        def on_blue_state_toggle(self):
                set_global_setting("BlueState", self.ui.BlueState.isChecked())

        def on_green_state_toggle(self):
                set_global_setting("GreenState", self.ui.GreenState.isChecked())

        def update_save_yaml_button_text(self):
            has_rows = False
            for i in range(self.ui.ScrollMain.widget().layout().count()):
                    row = self.ui.ScrollMain.widget().layout().itemAt(i).widget()
                    if row:
                            has_rows = True
                            break

            if has_rows:
                name = self.ui.YAMLLineEdit.text()
                game = self.ui.GameLineEdit.text()
                clean_game = sanitize_path_component(game)
                self.ui.SaveYamlButton.setText(f"Save YAML as '{name}-{clean_game}.yaml'")

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

        def check_if_rows_exist_and_set_text(self):
            has_rows = False
            for i in range(self.ui.ScrollMain.widget().layout().count()):
                row = self.ui.ScrollMain.widget().layout().itemAt(i).widget()
                if row:
                    has_rows = True
                    break

            if has_rows:
                self.ui.DescriptionLabel.setText("Description:")
            else:
                self.ui.DescriptionLabel.setText("Server Address:")
                self.ui.SaveYamlButton.setText(f"Extract Datapackage with Server Connection")

        def on_load_yaml_clicked(self):
            if hasattr(self, "current_yaml_path") and self.current_yaml_path:
                from load_yaml_data import load_yaml_UI
                selected_yaml_path = self.current_yaml_path

                with open(selected_yaml_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if isinstance(data, dict) and "game" in data:
                        base_game = str(data["game"])
                        clean_base_game = sanitize_path_component(base_game)
                        yaml_base_folder = os.path.join(get_exe_folder(), "YAMLS")
                        base_yaml_path = os.path.join(yaml_base_folder, f"{clean_base_game}_Template.yaml")

                        print("[INFO] Selected Slot YAML:", selected_yaml_path)
                        if config.debug_flag:
                                print("[INFO] Base Game YAML:", base_yaml_path)

                        if os.path.exists(base_yaml_path):
                            # WeightedSettingsEnabled toggle
                            self.ui.MainLayout.setStretch(0, 2)
                            self.ui.MainLayout.setStretch(1, 1)

                            load_yaml_UI(self, base_yaml_path, selected_yaml_path, base_game)
                            filter_rows(self, self.ui.SearchField.text())
                            name = self.ui.YAMLLineEdit.text()
                            game = self.ui.GameLineEdit.text()
                            clean_game = sanitize_path_component(game)
                            self.ui.SaveYamlButton.setText(f"Save YAML as '{name}-{clean_game}.yaml'")
                        else:
                            print(f"[mainwindow] [ERROR] Base YAML for game '{base_game}' not found: {base_yaml_path}")

                        from os.path import basename
                        yaml_name = basename(selected_yaml_path)
                        weighted_enabled = get_yaml_setting(yaml_name, "Enter Weighted Option Mode", False)
                        self.ui.WeightedSettingsEnabled.setChecked(weighted_enabled)
                    else:
                        print(f"[mainwindow] [ERROR] 'game' field missing in selected YAML: {selected_yaml_path}")
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
        create_datapackages_and_yaml_folders
    extract_datapackages()
    app = QApplication([])
    if not is_windows_11() or not is_dark_mode():
        apply_dark_theme(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
