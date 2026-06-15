import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolBar
)

from PyQt6.QtGui import QAction

from player import PlayerWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.player = PlayerWidget()

        self.setCentralWidget(self.player)

        toolbar = QToolBar()

        self.addToolBar(toolbar)

        open_video = QAction(
            "Open Video",
            self
        )

        open_video.triggered.connect(
            self.player.open_video
        )

        toolbar.addAction(open_video)

        open_subs = QAction(
            "Open Subs",
            self
        )

        open_subs.triggered.connect(
            self.player.open_subtitles
        )

        toolbar.addAction(open_subs)

        self.resize(1400, 800)


app = QApplication(sys.argv)

window = MainWindow()

window.show()

sys.exit(app.exec())