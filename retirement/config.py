import json
from pathlib import Path

def load_assumptions(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Cannot find assumptions file: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
