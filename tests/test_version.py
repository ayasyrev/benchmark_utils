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
