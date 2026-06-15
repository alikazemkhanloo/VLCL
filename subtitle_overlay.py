from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QFont, QColor, QTextLayout


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

        words = text.split()

        x = 40
        y = 20

        fm = self.font

        line_height = 50
        max_width = self.width() - 80

        for w in words:

            metrics = fm

            width = metrics.pointSize() * len(w) * 0.6 + 20
            height = line_height

            if x + width > max_width:
                x = 40
                y += line_height

            rect = QRectF(x, y, width, height)

            self.words.append(Word(w, rect))

            x += width + self.word_padding

    # -------------------------
    # PAINTING
    # -------------------------

    def paintEvent(self, event):

        if not self.visible_enabled:
            return

        painter = QPainter(self)

        painter.setFont(self.font)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        for word in self.words:

            painter.setPen(QColor("white"))

            painter.drawText(
                word.rect,
                Qt.AlignmentFlag.AlignCenter,
                word.text
            )

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

        print(f"Clicked word: {text}")

        # placeholder for dictionary / AI later