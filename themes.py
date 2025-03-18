# Dark Theme Stylesheet
dark_theme = """
    QWidget {
        background-color: #2b2b2b;
        color: #ffffff;
        font-family: Consolas, monospace;
        font-size: 1em; /* Scales with system DPI */
    }

    QLineEdit, QTextEdit, QComboBox, QSpinBox, QCheckBox, QPushButton {
        background-color: #3c3f41;
        color: #ffffff;
        border: 1px solid #555555;
        padding: 2px;
        border-radius: 4px;
    }

    QGroupBox {
        border: 1px solid #555555;
        border-radius: 4px;
        margin-top: 10px;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 5px;
        color: #ffffff;
    }

    QLabel {
        color: #ffffff;
    }
"""

# Notebook (Tab Widget) StyleSheet
notebook_style = """
    QTabBar::tab { 
        background-color: #3c3f41; 
        color: #ffffff; 
        padding: 2px 5px; 
        border: 1px solid #555555; 
    }
    QTabBar::tab:selected { 
        background-color: #4c4f51; 
        font-weight: bold; 
        border-bottom: 2px solid #ffffff; 
    }
"""
