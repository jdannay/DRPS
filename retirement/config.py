import json
from pathlib import Path
def load_assumptions(path):
    return json.loads(Path(path).read_text())
