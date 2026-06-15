from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont


class DictionaryPopup(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowStaysOnTopHint
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.label = QLabel()

        self.label.setStyleSheet("""
            QLabel {
                background-color: rgba(30, 30, 30, 50);
                color: white;
                padding: 10px;
                border-radius: 8px;
            }
        """)

        font = QFont("Arial", 14)
        self.label.setFont(font)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.hide()

    def show_word(self, data, global_pos: QPoint):

        text = f"""
<b>{data['text']}</b><br>
<lemma: {data['lemma']}> <br>
{data['meaning']}
"""

        self.label.setText(text)

        self.adjustSize()

        self.move(global_pos + QPoint(10, -80))

        self.show()

    def hide_popup(self):
        self.hide()