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

    /* Scroll Bar Customization */
    QScrollBar:vertical {
        border: none;
        background: #2b2b2b;
        width: 10px;
        margin: 0px 0px 0px 0px;
    }

    QScrollBar::handle:vertical {
        background: #00ccff;
        border-radius: 5px;
        min-height: 20px;
    }

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        background: none;
        border: none;
        height: 0px;
    }

    QScrollBar:horizontal {
        border: none;
        background: #2b2b2b;
        height: 10px;
        margin: 0px 0px 0px 0px;
    }

    QScrollBar::handle:horizontal {
        background: #00ccff;
        border-radius: 5px;
        min-width: 20px;
    }

    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        background: none;
        border: none;
        width: 0px;
    }

    QScrollBar::handle:hover {
        background: #00aacc;
    }

    QScrollBar::handle:pressed {
        background: #0088aa;
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
