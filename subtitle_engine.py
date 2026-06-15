import pysubs2


class SubtitleEngine:
    def __init__(self):
        self.subs = []

    def load(self, path):
        self.subs = pysubs2.load(path)

    def current_subtitle(self, ms):
        for line in self.subs:
            if line.start <= ms <= line.end:
                return line
        return None

    def subtitle_index(self, ms):
        for i, line in enumerate(self.subs):
            if line.start <= ms <= line.end:
                return i
        return -1

    def subtitle_by_index(self, idx):
        if 0 <= idx < len(self.subs):
            return self.subs[idx]
        return None