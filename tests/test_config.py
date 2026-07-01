from pathlib import Path
from retirement.config import load_assumptions

def test_load_assumptions():
    data = load_assumptions(Path("data") / "assumptions.json")
    assert data["portfolio"]["taxable"] == 1570000
