"""tests for version module"""

import importlib
import importlib.metadata as metadata

import benchmark_utils.version as version_mod


def test_version_from_metadata(monkeypatch):
    """Test that version comes from importlib.metadata when available"""

    def fake_version(_: str) -> str:
        return "9.9.9"

    monkeypatch.setattr(metadata, "version", fake_version)
    importlib.reload(version_mod)
    assert version_mod.__version__ == "9.9.9"


def test_version_from_pyproject(monkeypatch):
    """Test fallback to pyproject.toml when metadata unavailable"""

    def fake_version_raises(_: str) -> str:
        raise Exception("metadata unavailable")

    monkeypatch.setattr(metadata, "version", fake_version_raises)
    importlib.reload(version_mod)
    # Should fallback to pyproject.toml version
    assert version_mod.__version__ == "0.2.5b1"
