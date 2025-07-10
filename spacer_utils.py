from PySide6.QtWidgets import QSpacerItem, QSizePolicy

def move_spacer(layout):
    if layout.count() == 0:
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer_item)
        return

    last_item = layout.itemAt(layout.count() - 1)
    if isinstance(last_item, QSpacerItem):
        spacer_item = layout.takeAt(layout.count() - 1)
    else:
        spacer_item = None

    if spacer_item:
        layout.addItem(spacer_item)
    else:
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer_item)
