"""Pytest configuration — add src/ to Python path for test imports."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
