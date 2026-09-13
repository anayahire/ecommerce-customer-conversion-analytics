from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from quality_checks import load_raw, validate


def test_generated_raw_data_passes_validation():
    assert validate(load_raw()) == []
