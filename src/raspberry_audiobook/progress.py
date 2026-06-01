from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path


@dataclass
class PlaybackProgress:
    index: int
    position_ms: int


class ProgressStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._progress = self._load()

    def get(self, uid: str) -> PlaybackProgress | None:
        data = self._progress.get(uid)

        if not isinstance(data, dict):
            return None

        try:
            return PlaybackProgress(
                index=int(data["index"]),
                position_ms=int(data["position_ms"]),
            )
        except (KeyError, TypeError, ValueError):
            return None

    def save(self, uid: str, progress: PlaybackProgress) -> None:
        self._progress[uid] = asdict(progress)
        self._write()

    def clear(self, uid: str) -> None:
        if uid in self._progress:
            del self._progress[uid]
            self._write()

    def _load(self) -> dict:
        if not self.path.exists():
            return {}

        try:
            with self.path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            return {}

        if not isinstance(data, dict):
            return {}

        return data

    def _write(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)

        with self.path.open("w", encoding="utf-8") as file:
            json.dump(self._progress, file, indent=2)
            file.write("\n")
