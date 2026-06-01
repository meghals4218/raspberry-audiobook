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


def enable_motor(
    *,
    motor_pins: tuple[int, int, int, int],
    motor_rpm: float,
    motor_reverse: bool,
) -> object:
    from .motor import StepperMotor

    return StepperMotor(
        pins=motor_pins,
        rpm=motor_rpm,
        reverse=motor_reverse,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the Raspberry Pi audiobook player."
    )
    parser.add_argument("--config", default="config/books.yaml")
    parser.add_argument(
        "--progress",
        default=None,
        help="Path to the JSON file used to save playback progress.",
    )
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
    parser.add_argument(
        "--motor-pins",
        nargs=4,
        type=int,
        default=None,
        metavar=("IN1", "IN2", "IN3", "IN4"),
        help="Enable a 4-wire stepper motor using these GPIO pins.",
    )
    parser.add_argument("--motor-rpm", type=float, default=5.0)
    parser.add_argument("--motor-reverse", action="store_true")
    args = parser.parse_args()

    motor = None
    if args.motor_pins is not None:
        motor = enable_motor(
            motor_pins=tuple(args.motor_pins),
            motor_rpm=args.motor_rpm,
            motor_reverse=args.motor_reverse,
        )

    app = AudiobookApp(
        config_path=Path(args.config),
        use_mock=args.mock,
        progress_path=Path(args.progress) if args.progress else None,
        on_playback_start=motor.start if motor is not None else None,
        on_playback_stop=motor.stop if motor is not None else None,
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

    try:
        app.run()
    finally:
        if motor is not None:
            motor.close()


if __name__ == "__main__":
    main()
