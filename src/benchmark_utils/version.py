from __future__ import annotations

import importlib.util
import warnings
from pathlib import Path

_VERSION_UNKNOWN = "UNKNOWN"


def _load_tomllib():
    """Load tomllib or tomli module with fallback and warning.

    Returns:
        tomllib or tomli module, or None if neither available.

    Raises:
        Warning: If both tomllib and tomli are unavailable.
    """
    if importlib.util.find_spec("tomllib") is not None:
        import tomllib

        return tomllib
    if importlib.util.find_spec("tomli") is not None:
        import tomli as tomllib

        return tomllib
    warnings.warn("Both tomllib (Python 3.11+) and tomli are unavailable", RuntimeWarning, stacklevel=3)
    return None


def _find_pyproject_toml(max_depth: int = 5) -> Path | None:
    """Find pyproject.toml by walking up directory tree.

    Args:
        max_depth: Maximum number of parent directories to search.

    Returns:
        Path to pyproject.toml if found, None otherwise.
    """
    current = Path(__file__).resolve().parent
    for _ in range(max_depth):
        pyproject = current / "pyproject.toml"
        if pyproject.exists():
            return pyproject
        if current.parent == current:
            break
        current = current.parent
    return None


def _read_version_from_pyproject() -> str:
    """Read version from pyproject.toml file.

    Returns:
        Version string from pyproject.toml, or _VERSION_UNKNOWN if not found.

    Emits:
        Warning: If pyproject.toml is missing, cannot be read,
                 contains invalid TOML, or missing [project].version.
    """
    pyproject_path = _find_pyproject_toml()
    if pyproject_path is None:
        warnings.warn("pyproject.toml not found in parent directories", RuntimeWarning, stacklevel=3)
        return _VERSION_UNKNOWN

    toml_lib = _load_tomllib()
    if toml_lib is None:
        return _VERSION_UNKNOWN

    try:
        with open(pyproject_path, "rb") as f:
            data = toml_lib.load(f)
    except OSError as e:
        warnings.warn(f"Failed to read {pyproject_path}: {e}", RuntimeWarning, stacklevel=3)
        return _VERSION_UNKNOWN
    except toml_lib.TOMLDecodeError as e:
        warnings.warn(f"Failed to parse {pyproject_path}: {e}", RuntimeWarning, stacklevel=3)
        return _VERSION_UNKNOWN

    if "project" not in data:
        warnings.warn(f"No [project] section in {pyproject_path}", RuntimeWarning, stacklevel=3)
        return _VERSION_UNKNOWN
    if "version" not in data["project"]:
        warnings.warn(f"No version field in [project] section of {pyproject_path}", RuntimeWarning, stacklevel=3)
        return _VERSION_UNKNOWN
    return data["project"]["version"]


def get_version() -> str:
    """Get the package version.

    First tries importlib.metadata.version("benchmark_utils").
    Falls back to reading pyproject.toml if metadata unavailable.
    Returns _VERSION_UNKNOWN as ultimate fallback.

    Returns:
        Version string.
    """
    try:
        from importlib.metadata import version

        return version("benchmark_utils")
    except importlib.metadata.PackageNotFoundError:
        return _read_version_from_pyproject()


__version__ = get_version()  # pragma: no cover
