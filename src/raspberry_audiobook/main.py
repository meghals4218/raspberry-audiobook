from pathlib import Path
import argparse

from .app import AudiobookApp


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/books.yaml")
    parser.add_argument("--mock", action="store_true")
    args = parser.parse_args()

    app = AudiobookApp(
        config_path=Path(args.config),
        use_mock=args.mock,
    )
    app.run_once()


if __name__ == "__main__":
    main()