"""tests for version module"""

import importlib.metadata as metadata
import importlib.util
import warnings

import benchmark_utils.version as version_mod


def test_version_from_metadata(monkeypatch):
    """Test that version comes from importlib.metadata when available"""

    # Mock importlib.metadata.version at the module level
    def fake_version(_: str) -> str:
        return "9.9.9"

    import importlib.metadata as metadata_mod

    monkeypatch.setattr(metadata_mod, "version", fake_version)

    # Call get_version directly
    result = version_mod.get_version()
    assert result == "9.9.9"


def test_version_from_pyproject(monkeypatch):
    """Test fallback to pyproject.toml when metadata unavailable"""
    # Read expected version from pyproject.toml to avoid brittleness
    pyproject_path = version_mod._find_pyproject_toml()
    assert pyproject_path is not None, "pyproject.toml not found for test"

    toml_lib = version_mod._load_tomllib()
    assert toml_lib is not None, "toml library not found for test"

    with open(pyproject_path, "rb") as f:
        expected_version = toml_lib.load(f)["project"]["version"]

    # Mock metadata to raise error
    def fake_version_raises(_: str) -> str:
        raise metadata.PackageNotFoundError("metadata unavailable")

    import importlib.metadata as metadata_mod

    monkeypatch.setattr(metadata_mod, "version", fake_version_raises)

    result = version_mod.get_version()
    assert result == expected_version


def test_missing_pyproject_toml(tmp_path, monkeypatch):
    """Test that missing pyproject.toml returns UNKNOWN with warning"""

    def fake_find_pyproject():
        return None

    monkeypatch.setattr(version_mod, "_find_pyproject_toml", fake_find_pyproject)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = version_mod._read_version_from_pyproject()
        assert result == "UNKNOWN"
        assert any("pyproject.toml not found" in str(warn.message) for warn in w)


def test_malformed_toml(tmp_path, monkeypatch):
    """Test that malformed TOML returns UNKNOWN with warning"""
    bad_toml = tmp_path / "pyproject.toml"
    bad_toml.write_text("[invalid\nunclosed section")

    def fake_find_pyproject():
        return bad_toml

    monkeypatch.setattr(version_mod, "_find_pyproject_toml", fake_find_pyproject)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = version_mod._read_version_from_pyproject()
        assert result == "UNKNOWN"
        assert any("Failed to parse" in str(warn.message) for warn in w)


def test_missing_tomllib_and_tomli(monkeypatch):
    """Test that missing tomllib/tomli returns UNKNOWN with warning"""

    import sys

    original_modules = {}
    for mod in ["tomllib", "tomli"]:
        if mod in sys.modules:
            original_modules[mod] = sys.modules[mod]
            del sys.modules[mod]

    def fake_find_spec(name):
        if name in ("tomllib", "tomli"):
            return None
        return original_find_spec(name)

    original_find_spec = importlib.util.find_spec
    monkeypatch.setattr(importlib.util, "find_spec", fake_find_spec)

    try:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = version_mod._read_version_from_pyproject()
            assert result == "UNKNOWN"
            assert any("tomllib" in str(warn.message) and "tomli" in str(warn.message) for warn in w)
    finally:
        sys.modules.update(original_modules)


def test_missing_version_field(tmp_path, monkeypatch):
    """Test that missing [project].version returns UNKNOWN with warning"""
    no_version = tmp_path / "pyproject.toml"
    no_version.write_text("[project]\nname = 'test'")

    def fake_find_pyproject():
        return no_version

    monkeypatch.setattr(version_mod, "_find_pyproject_toml", fake_find_pyproject)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = version_mod._read_version_from_pyproject()
        assert result == "UNKNOWN"
        assert any("No version field" in str(warn.message) for warn in w)
