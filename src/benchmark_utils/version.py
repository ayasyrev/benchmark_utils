from __future__ import annotations

from pathlib import Path


def _read_version_from_pyproject() -> str:
    """Read version from pyproject.toml file.

    Returns:
        Version string from pyproject.toml, or '0.0.0' if not found.
    """
    pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
    try:
        import tomllib

        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)
            return data.get("project", {}).get("version", "0.0.0")
    except (FileNotFoundError, OSError):
        return "0.0.0"


def get_version() -> str:
    """Get the package version.

    First tries importlib.metadata.version("benchmark_utils").
    Falls back to reading pyproject.toml if metadata unavailable.
    Returns "0.0.0" as ultimate fallback.

    Returns:
        Version string.
    """
    try:
        from importlib.metadata import version

        return version("benchmark_utils")
    except Exception:
        return _read_version_from_pyproject()


__version__ = get_version()  # pragma: no cover
