@echo off
cd /d %~dp0
pyinstaller --onefile --add-data "Setup;Setup" --add-data "YAML;YAML" yaml_editor.py
pause
