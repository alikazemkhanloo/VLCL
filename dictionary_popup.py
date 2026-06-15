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
        print('data',data)
        status = data.get('status', 'error')
        code = data.get('error_code', None)
        result = data['data']
        print('result', result)

        if status == 'error':
            text = f"""
                <b>Error:</b><br>
                <i>{code}</i><br>
            """
        else:
            text = f"""
                <b>{result['word']}</b><br>
                {result['definition']}
            """

        self.label.setText(text)

        self.adjustSize()

        self.move(global_pos + QPoint(10, -80))

        self.show()

    def hide_popup(self):
        self.hide()