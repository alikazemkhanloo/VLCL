import sys
import vlc

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFileDialog
)

from PyQt6.QtCore import (
    QTimer,
    Qt
)

from subtitle_engine import SubtitleEngine
from subtitle_overlay import SubtitleOverlay


class PlayerWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("LinguaPlayer")

        self.instance = vlc.Instance()
        self.mediaplayer = self.instance.media_player_new()

        self.video_frame = QWidget(self)

        self.overlay = SubtitleOverlay(self)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.video_frame)

        self.setLayout(layout)

        self.sub_engine = SubtitleEngine()

        self.current_sub = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_subtitles)
        self.timer.start(100)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.overlay.setGeometry(
            100,
            self.height() - 180,
            self.width() - 200,
            120
        )

    def open_video(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Video"
        )

        if not path:
            return

        media = self.instance.media_new(path)

        self.mediaplayer.set_media(media)

        if sys.platform == "darwin":
            self.mediaplayer.set_nsobject(
                int(self.video_frame.winId())
            )

        self.mediaplayer.play()

    def open_subtitles(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Subtitle",
            filter="Subtitles (*.srt)"
        )

        if path:
            self.sub_engine.load(path)

    def update_subtitles(self):

        if not self.mediaplayer.is_playing():
            return

        current_ms = self.mediaplayer.get_time()

        line = self.sub_engine.current_subtitle(
            current_ms
        )

        if line:

            if self.current_sub != line:

                self.current_sub = line

                self.overlay.set_subtitle(
                    line.text.replace("\\N", "\n")
                )

        else:
            self.overlay.set_subtitle("")
            self.current_sub = None

    def replay_current_subtitle(self):

        if not self.current_sub:
            return

        self.mediaplayer.set_time(
            self.current_sub.start
        )

    def keyPressEvent(self, event):

        if event.key() == Qt.Key.Key_S:
            self.overlay.toggle()

        elif event.key() == Qt.Key.Key_R:
            self.replay_current_subtitle()