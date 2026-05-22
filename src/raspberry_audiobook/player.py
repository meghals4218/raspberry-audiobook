from pathlib import Path
import subprocess


class AudioPlayer:
    def play_folder(self, folder: Path) -> None:
        files = sorted(folder.glob("*.mp3"))

        if not files:
            print(f"No MP3 files found in {folder}")
            return

        for file in files:
            print(f"Playing {file}")
            subprocess.run(["mpg123", str(file)], check=False)