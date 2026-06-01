from pathlib import Path
from collections.abc import Callable
import time

from .config import load_books
from .nfc import MockNFCReader, RC522Reader
from .player import AudioPlayer
from .progress import PlaybackProgress, ProgressStore


class AudiobookApp:
    def __init__(
        self,
        config_path: Path,
        use_mock: bool = False,
        progress_path: Path | None = None,
        on_playback_start: Callable[[], None] | None = None,
        on_playback_stop: Callable[[], None] | None = None,
    ) -> None:
        self.books = load_books(config_path)
        self.reader = MockNFCReader() if use_mock else RC522Reader()
        self.player = AudioPlayer()
        self.progress = ProgressStore(progress_path or config_path.with_name("progress.json"))
        self.current_uid: str | None = None
        self.on_playback_start = on_playback_start
        self.on_playback_stop = on_playback_stop

    def run(self) -> None:
        try:
            while True:
                try:
                    self.run_once()
                except Exception as error:
                    print(f"Error occurred: {error}")
        except KeyboardInterrupt:
            print("Exiting...")
        finally:
            self.save_current_progress()
            self.stop_playback_accessories()
            self.player.stop()

    def run_once(self) -> None:
        uid = self.reader.read_uid()
        print(f"Read UID: {uid}")

        book = self.books.get(uid)

        if book is None:
            print("Unknown tag.")
            return

        self.current_uid = uid
        title = book["title"]
        path = Path(book["path"])

        print(f"Selected: {title}")
        self.player.load_folder(path)

        if not self.player.playlist:
            print("No MP3 files found for this book.")
            self.current_uid = None
            return

        saved_progress = self.progress.get(uid)
        if saved_progress is not None:
            self.player.index = max(
                0,
                min(saved_progress.index, len(self.player.playlist) - 1),
            )
            print(f"Resuming from saved spot: chapter {self.player.index + 1}")

        start_ms = max(0, saved_progress.position_ms) if saved_progress is not None else 0
        self.player.play_current(start_ms=start_ms)
        self.start_playback_accessories()

        last_save = time.monotonic()

        def save_progress(index: int, position_ms: int) -> None:
            nonlocal last_save

            if time.monotonic() - last_save < 5:
                return

            self.progress.save(uid, PlaybackProgress(index, position_ms))
            last_save = time.monotonic()

        try:
            finished = self.player.play_until_finished(on_progress=save_progress)
        finally:
            self.stop_playback_accessories()

        if finished:
            self.progress.clear(uid)
            print("Playback finished. Ready for next tag.")
        else:
            self.save_current_progress()
            print("Playback stopped. Saved progress.")

        self.current_uid = None

    def save_current_progress(self) -> None:
        if self.current_uid is None:
            return

        position = self.player.current_position()
        if position is None:
            return

        index, position_ms = position
        self.progress.save(self.current_uid, PlaybackProgress(index, position_ms))

    def start_playback_accessories(self) -> None:
        if self.on_playback_start is not None:
            self.on_playback_start()

    def stop_playback_accessories(self) -> None:
        if self.on_playback_stop is not None:
            self.on_playback_stop()
