from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QFontMetrics, QPainter, QFont, QColor, QTextLayout

class Word:
    def __init__(self, text, rect):
        self.text = text
        self.rect = rect


class SubtitleOverlay(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.words = []
        self.text = ""

        self.visible_enabled = True

        self.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents,
            False
        )

        self.font = QFont("Arial", 28)
        self.word_padding = 6

        self.clicked_callback = None
        self.popup_callback = None
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)
        self.setAutoFillBackground(False)
        # self.setStyleSheet("""
        #     background-color: rgba(255, 0, 0, 80);
        # """)
        
    # -------------------------
    # PUBLIC API
    # -------------------------

    def set_subtitle(self, text):
        if not self.visible_enabled:
            self.words = []
            self.text = ""
            self.update()
            return

        self.text = text.replace("\\N", " ")

        self._layout_words(self.text)
        self.update()

    def toggle(self):
        self.visible_enabled = not self.visible_enabled

        if not self.visible_enabled:
            self.words = []
            self.text = ""

        self.update()

    # -------------------------
    # LAYOUT ENGINE
    # -------------------------

    def _layout_words(self, text):
        self.words = []

        font = self.font
        metrics = QFontMetrics(font)

        layout = QTextLayout(text, font)
        layout.beginLayout()

        x, y = 40, 20
        max_width = self.width() - 80
        line_height = metrics.height() + 10

        line = layout.createLine()
        while line.isValid():
            line.setLineWidth(max_width)

            line_natural_width = line.naturalTextWidth()

            if x + line_natural_width > max_width:
                x = 40
                y += line_height

            start = line.textStart()
            length = line.textLength()
            segment = text[start:start+length]

            words = segment.split()

            cursor_x = x

            for w in words:
                w_width = metrics.horizontalAdvance(w)

                rect = QRectF(cursor_x, y, w_width, line_height)

                self.words.append(Word(w, rect))

                cursor_x += w_width + 6

            x = 40
            y += line_height

            line = layout.createLine()

        layout.endLayout()
    # -------------------------
    # PAINTING
    # -------------------------

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)

        painter.fillRect(self.rect(), QColor(0, 0, 0, 0))  # HARD CLEAR

        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)

        painter.setFont(self.font)

        for word in self.words:
            painter.setPen(QColor("white"))
            painter.drawRect(word.rect)
            painter.drawText(word.rect, Qt.AlignmentFlag.AlignCenter, word.text) 
    # -------------------------
    # INTERACTION
    # -------------------------

    def mousePressEvent(self, event):

        if not self.visible_enabled:
            return

        pos = event.position()

        for word in self.words:
            if word.rect.contains(pos):

                self.on_word_clicked(word.text, word.rect)
                break

    def on_word_clicked(self, text, rect):

        # data = self.dictionary.analyze(text)

        global_pos = self.mapToGlobal(
            rect.topLeft().toPoint()
        )

        # if self.popup_callback:
        #     self.popup_callback(data, global_pos)