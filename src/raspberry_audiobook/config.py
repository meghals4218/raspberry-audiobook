from pathlib import Path
import yaml


def load_books(config_path: Path) -> dict:
    with config_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return data["books"]