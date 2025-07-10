# description.py
def set_description_text(main_window, text: str):
    main_window.ui.DescriptionText.setPlainText(text)

def show_description_text(main_window, visible: bool):
    main_window.ui.DescriptionText.setVisible(visible)
