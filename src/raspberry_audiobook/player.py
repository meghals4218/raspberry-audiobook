from pathlib import Path
import time

import vlc


class AudioPlayer:
    def __init__(self) -> None:
        self.instance = vlc.Instance(
            "--aout=alsa",
            "--alsa-audio-device=default",
            "--codec=avcodec,any",
            "--quiet",
        )
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

    def play_until_finished(self, poll_seconds: float = 0.5) -> None:
        while self.playlist:
            state = self.player.get_state()

            if state == vlc.State.Ended:
                if self.index >= len(self.playlist) - 1:
                    return

                self.index += 1
                self.play_current()
                continue

            if state in {vlc.State.Stopped, vlc.State.Error}:
                return

            time.sleep(poll_seconds)

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

        target = max(0, current + seconds * 1000)
        self.player.set_time(target)
        print(f"Seek: {seconds:+d}s {self._progress_bar(target)}")

    def next_chapter(self) -> None:
        if self.index < len(self.playlist) - 1:
            self.index += 1
            self.play_current()

    def prev_chapter(self) -> None:
        if self.index > 0:
            self.index -= 1
            self.play_current()

    def _format_time(self, milliseconds: int) -> str:
        total_seconds = milliseconds // 1000
        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)

        if hours:
            return f"{hours}:{minutes:02d}:{seconds:02d}"

        return f"{minutes}:{seconds:02d}"

    def _progress_bar(self, position: int, width: int = 24) -> str:
        length = self.player.get_length()

        if length <= 0:
            return f"[{'?' * width}] {self._format_time(position)}"

        clamped_position = max(0, min(position, length))
        filled = round((clamped_position / length) * width)
        bar = "#" * filled + "-" * (width - filled)

        return (
            f"[{bar}] "
            f"{self._format_time(clamped_position)} / {self._format_time(length)}"
        )
