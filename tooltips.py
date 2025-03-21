from PyQt5.QtGui import QCursor, QTextDocument, QGuiApplication
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtCore import Qt
import os

class HoverTooltip(QLabel):
    """Tooltip overlay widget for displaying information over other widgets."""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: #444444; color: #50c878; padding: 5px; font-size: 10pt;")
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setTextFormat(Qt.RichText)  # Enable multi-line text
        self.setWordWrap(False)

        # Preserve proper newlines and formatting
        formatted_text = self.format_tooltip_text(text)

        self.setText(formatted_text)

        # Set a very wide max width to avoid overflow issues
        self.max_width = 800  # Make tooltip really wide
        doc = QTextDocument()
        doc.setHtml(formatted_text)
        doc.setTextWidth(self.max_width)
        self.resize(int(doc.idealWidth()), int(doc.size().height()))

        self.hide()

    def format_tooltip_text(self, text):
        """Formats tooltip text by bolding and underlining any text before a colon, while keeping '# ' untouched."""
        lines = text.split("\n")
        formatted_lines = []

        for line in lines:
            stripped_line = line.strip()

            if stripped_line.startswith("# "):  # Check if it starts with a comment
                comment_prefix = "# "
                content = stripped_line[2:].strip()  # Remove the `# ` part
                
                if ":" in content:
                    parts = content.split(":", 1)  # Split at the first colon
                    bolded_part = f"<b><u>{parts[0].strip()}</u></b>"  # Bold and underline
                    formatted_line = f"{comment_prefix}{bolded_part}: {parts[1].strip()}"
                else:
                    formatted_line = line.strip()  # Keep the line unchanged if no colon exists
            else:
                formatted_line = line.strip()

            formatted_lines.append(formatted_line)

        # Preserve newlines properly
        return "<br>".join(formatted_lines)

    def show_tooltip(self, pos):
        """Display tooltip near cursor position, ensuring it stays on screen."""
        self.adjustSize()  # Ensure correct tooltip size before positioning
        self.resize(self.sizeHint())  # Explicitly resize to fit text

        screen = QGuiApplication.screenAt(pos)
        if screen is None:
            screen = QGuiApplication.primaryScreen()  # Fallback to primary if detection fails
        screen_rect = screen.availableGeometry()

        tooltip_rect = self.frameGeometry()

        # Position tooltip above the cursor
        pos.setY(pos.y() - tooltip_rect.height() - 10)
        pos.setX(pos.x() + 7)

        # Ensure tooltip does not go off-screen horizontally
        if pos.x() + tooltip_rect.width() > screen_rect.right():
            pos.setX(screen_rect.right() - tooltip_rect.width() - 5)  # Shift left if too wide

        if pos.x() < screen_rect.left():
            pos.setX(screen_rect.left() + 5)  # Shift right if too far left

        # Ensure tooltip does not go off-screen vertically
        if pos.y() < screen_rect.top():
            pos.setY(screen_rect.top() + 5)  # Shift down if needed

        self.move(pos)
        self.show()

    def hide_tooltip(self):
        """Hide the tooltip"""
        self.hide()


class TooltipButton(QPushButton):
    """Button that displays a tooltip when hovered or clicked, keeping it open until clicked again or another tooltip is shown."""
    
    active_tooltip = None  # Track the currently active tooltip

    def __init__(self, tooltip_text, parent=None):
        super().__init__("?", parent)
        self.setFixedSize(20, 20)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                font-weight: bold;
                color: #ffffff;
            }
            QPushButton:hover {
                color: #00ccff;
            }
        """)

        self.tooltip = HoverTooltip(tooltip_text, parent)
        self.tooltip.hide()

        self.clicked.connect(self.toggle_tooltip)

    def enterEvent(self, event):
        """Show tooltip when mouse enters button (only if no other tooltip is open)"""
        if TooltipButton.active_tooltip is None:
            self.tooltip.show_tooltip(QCursor.pos())

    def leaveEvent(self, event):
        """Hide tooltip when mouse leaves button (only if not pinned open)"""
        if TooltipButton.active_tooltip is None:
            self.tooltip.hide_tooltip()

    def toggle_tooltip(self):
        """Toggle tooltip visibility when button is clicked"""
        if TooltipButton.active_tooltip == self.tooltip:
            self.tooltip.hide_tooltip()
            TooltipButton.active_tooltip = None  # Reset active tooltip
        else:
            # Hide any previously active tooltip
            if TooltipButton.active_tooltip is not None:
                TooltipButton.active_tooltip.hide_tooltip()

            # Show the new tooltip and set it as active
            self.tooltip.show_tooltip(QCursor.pos())
            TooltipButton.active_tooltip = self.tooltip

    @staticmethod
    def hide_active_tooltip():
        if TooltipButton.active_tooltip is not None:
            TooltipButton.active_tooltip.hide_tooltip()
            TooltipButton.active_tooltip = None

