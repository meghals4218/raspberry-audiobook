from __future__ import annotations

from collections.abc import Sequence
import threading
import time

from gpiozero import Device, OutputDevice
from gpiozero.pins.lgpio import LGPIOFactory


Device.pin_factory = LGPIOFactory()


class StepperMotor:
    HALF_STEP_SEQUENCE = (
        (1, 0, 0, 0),
        (1, 1, 0, 0),
        (0, 1, 0, 0),
        (0, 1, 1, 0),
        (0, 0, 1, 0),
        (0, 0, 1, 1),
        (0, 0, 0, 1),
        (1, 0, 0, 1),
    )

    def __init__(
        self,
        pins: Sequence[int],
        *,
        rpm: float = 5.0,
        reverse: bool = False,
        steps_per_rotation: int = 4096,
    ) -> None:
        if len(pins) != 4:
            raise ValueError("Stepper motor needs exactly four GPIO pins.")
        if rpm <= 0:
            raise ValueError("Stepper motor RPM must be greater than zero.")

        self.coils = [OutputDevice(pin, initial_value=False) for pin in pins]
        self.rpm = rpm
        self.reverse = reverse
        self.steps_per_rotation = steps_per_rotation
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return

        self._stop.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        print("Motor: started")

    def stop(self) -> None:
        was_running = self._thread is not None and self._thread.is_alive()
        self._stop.set()

        if self._thread is not None:
            self._thread.join(timeout=1)
            self._thread = None

        self._release()

        if was_running:
            print("Motor: stopped")

    def close(self) -> None:
        self.stop()

        for coil in self.coils:
            coil.close()

    def _run(self) -> None:
        sequence = self.HALF_STEP_SEQUENCE

        if self.reverse:
            sequence = tuple(reversed(sequence))

        delay = max(0.001, 60 / (self.rpm * self.steps_per_rotation))

        while not self._stop.is_set():
            for step in sequence:
                if self._stop.is_set():
                    break

                self._apply_step(step)
                time.sleep(delay)

    def _apply_step(self, step: Sequence[int]) -> None:
        for coil, value in zip(self.coils, step):
            if value:
                coil.on()
            else:
                coil.off()

    def _release(self) -> None:
        for coil in self.coils:
            coil.off()
