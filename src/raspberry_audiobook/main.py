from pathlib import Path
import argparse

from .app import AudiobookApp


def enable_rotary_controls(
    app: AudiobookApp,
    *,
    volume_pins: tuple[int, int],
    seek_pins: tuple[int, int],
    volume_step: int,
    seek_seconds: int,
    initial_volume: int,
) -> list[object]:
    from .seek import SeekController
    from .volume import VolumeController

    volume = VolumeController(
        on_change=app.player.set_volume,
        a_pin=volume_pins[0],
        b_pin=volume_pins[1],
        initial_volume=initial_volume,
        step=volume_step,
    )
    seek = SeekController(
        on_seek=app.player.seek_relative,
        a_pin=seek_pins[0],
        b_pin=seek_pins[1],
        step_seconds=seek_seconds,
    )
    return [volume, seek]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the Raspberry Pi audiobook player."
    )
    parser.add_argument("--config", default="config/books.yaml")
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Read NFC UIDs from the terminal instead of the RC522 reader.",
    )
    parser.add_argument(
        "--no-controls",
        action="store_true",
        help="Do not initialize GPIO rotary encoders.",
    )
    parser.add_argument("--volume-pins", nargs=2, type=int, default=(16, 20))
    parser.add_argument("--seek-pins", nargs=2, type=int, default=(19, 26))
    parser.add_argument("--volume-step", type=int, default=5)
    parser.add_argument("--seek-seconds", type=int, default=10)
    parser.add_argument("--initial-volume", type=int, default=50)
    args = parser.parse_args()

    app = AudiobookApp(
        config_path=Path(args.config),
        use_mock=args.mock,
    )

    _controls = []
    if not args.no_controls:
        _controls = enable_rotary_controls(
            app,
            volume_pins=tuple(args.volume_pins),
            seek_pins=tuple(args.seek_pins),
            volume_step=args.volume_step,
            seek_seconds=args.seek_seconds,
            initial_volume=args.initial_volume,
        )

    app.run()


if __name__ == "__main__":
    main()
