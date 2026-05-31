from pathlib import Path
import argparse

from .app import AudiobookApp
from .volume import VolumeController


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/books.yaml")
    parser.add_argument("--mock", action="store_true")
    args = parser.parse_args()
    
    volume = VolumeController()

    app = AudiobookApp(
        config_path=Path(args.config),
        use_mock=args.mock,
    )
    app.run()


if __name__ == "__main__":
    main()