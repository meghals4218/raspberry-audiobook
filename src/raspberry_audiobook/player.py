# player.py

from pathlib import Path
import vlc
import time


class AudioPlayer:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        self.playlist = []
        self.index = 0

    def load_folder(self, folder: Path):
        self.playlist = sorted(folder.glob("*.mp3"))
        self.index = 0

    def play_current(self):
        if not self.playlist:
            return

        media = self.instance.media_new(str(self.playlist[self.index]))
        self.player.set_media(media)
        self.player.play()

        time.sleep(0.5)

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def set_volume(self, volume):
        self.player.audio_set_volume(volume)

    def seek_relative(self, seconds):
        current = self.player.get_time()
        self.player.set_time(current + seconds * 1000)

    def next_chapter(self):
        if self.index < len(self.playlist) - 1:
            self.index += 1
            self.play_current()

    def prev_chapter(self):
        if self.index > 0:
            self.index -= 1
            self.play_current()