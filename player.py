import sys
import vlc

from PyQt6.QtWidgets import (
    QSizePolicy,
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
from dictionary_popup import DictionaryPopup

class PlayerWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("LinguaPlayer")

        self.instance = vlc.Instance()
        self.mediaplayer = self.instance.media_player_new()

        self.video_frame = QWidget(self)
        self.overlay = SubtitleOverlay(self)
        self.overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.overlay.raise_()
        self.overlay.show()
        self.overlay.popup_callback = self.show_dictionary

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.video_frame)
        self.video_frame.setMinimumSize(1, 1)
        self.video_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        self.setLayout(layout)

        self.sub_engine = SubtitleEngine()

        self.current_sub = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_subtitles)
        self.timer.start(100)

        self.popup = DictionaryPopup()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()

    def show_dictionary(self, data, pos):
        self.popup.show_word(data, pos)


    def resizeEvent(self, event):
        super().resizeEvent(event)



        self.video_frame.setGeometry(self.rect())

        self.overlay.setGeometry(self.video_frame.geometry())
        # self.overlay.setGeometry(self.video_frame.rect())
        self.overlay.raise_()

        print("[Overlay] visible:", self.overlay.isVisible())
        print("[Overlay] geometry:", self.overlay.geometry())


        
    def open_video(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Video"
        )

        if not path:
            return

        media = self.instance.media_new(path)

        media.add_option("no-sub-autodetect-file")
        media.add_option("no-spu")

        self.mediaplayer.set_media(media)
        self.mediaplayer.video_set_spu(-1)
        if sys.platform == "darwin":
            self.video_frame.winId()  # force native handle creation
            self.mediaplayer.set_nsobject(int(self.video_frame.winId()))
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