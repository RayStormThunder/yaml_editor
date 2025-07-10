import sys
import os

# Get the running directory safely
if getattr(sys, 'frozen', False):  # Running from PyInstaller bundle
    base_dir = sys._MEIPASS
    exe_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    exe_dir = base_dir  # Same in normal mode

def get_base_folder():
    return base_dir

def get_exe_folder():
    return exe_dir

def get_gui_data_file():
    return os.path.join(get_base_folder(), "gui_data.json")
