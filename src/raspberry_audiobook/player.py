from pathlib import Path
import time

import vlc


class AudioPlayer:
    def __init__(self) -> None:
        self.instance = vlc.Instance("--aout=alsa", "--alsa-audio-device=default")
        self.player = self.instance.media_player_new()

        self.playlist: list[Path] = []
        self.index = 0

    def load_folder(self, folder: Path) -> None:
        self.playlist = sorted(folder.glob("*.mp3"))
        self.index = 0

    def play_current(self) -> None:
        if not self.playlist:
            return

        media = self.instance.media_new(str(self.playlist[self.index]))
        self.player.set_media(media)
        self.player.play()

        time.sleep(0.5)

    def pause(self) -> None:
        self.player.pause()

    def stop(self) -> None:
        self.player.stop()

    def set_volume(self, volume: int) -> None:
        self.player.audio_set_volume(volume)

    def seek_relative(self, seconds: int) -> None:
        current = self.player.get_time()
        if current < 0:
            return

        self.player.set_time(max(0, current + seconds * 1000))

    def next_chapter(self) -> None:
        if self.index < len(self.playlist) - 1:
            self.index += 1
            self.play_current()

    def prev_chapter(self) -> None:
        if self.index > 0:
            self.index -= 1
            self.play_current()
