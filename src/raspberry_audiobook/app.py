from pathlib import Path

from .config import load_books
from .nfc import MockNFCReader, RC522Reader
from .player import AudioPlayer


class AudiobookApp:
    def __init__(self, config_path: Path, use_mock: bool = False):
        self.books = load_books(config_path)
        self.reader = MockNFCReader() if use_mock else RC522Reader()
        self.player = AudioPlayer()

    def run_once(self) -> None:
        uid = self.reader.read_uid()
        print(f"Read UID: {uid}")

        book = self.books.get(uid)

        if book is None:
            print("Unknown tag.")
            return

        title = book["title"]
        path = Path(book["path"])

        print(f"Selected: {title}")
        self.player.play_folder(path)