# Version From Pyproject Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace the hardcoded `__version__` with a runtime value sourced from package metadata, with a fallback to `pyproject.toml`.

**Architecture:** At import time, `get_version()` tries `importlib.metadata.version("benchmark_utils")`. If metadata is unavailable, it reads `pyproject.toml` near the repo root and extracts `[project].version`. If neither source is available, it returns `"0.0.0"` to keep imports safe. The public API remains `benchmark_utils.__version__`.

**Tech Stack:** Python 3.10+, stdlib `importlib.metadata`, `tomllib` (3.11+), optional minimal parser fallback.

---

### Task 1: Add runtime version resolution in version module

**Files:**
- Modify: `src/benchmark_utils/version.py`

**Step 1: Write the failing test**
Create `tests/test_version.py` with a test that asserts `__version__` matches a stubbed `importlib.metadata.version`.

```python
import importlib
import importlib.metadata as metadata

import benchmark_utils.version as version_mod


def test_version_from_metadata(monkeypatch):
    def fake_version(_: str) -> str:
        return "9.9.9"

    monkeypatch.setattr(metadata, "version", fake_version)
    importlib.reload(version_mod)
    assert version_mod.__version__ == "9.9.9"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_version.py::test_version_from_metadata -v`  
Expected: FAIL because `__version__` is still hardcoded.

**Step 3: Write minimal implementation**

In `src/benchmark_utils/version.py`, implement:

```python
from __future__ import annotations

from importlib import metadata
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None


def _read_version_from_pyproject() -> str | None:
    pyproject_path = Path(__file__).resolve().parents[2] / "pyproject.toml"
    if not pyproject_path.exists():
        return None

    data: dict[str, object] | None = None
    if tomllib is not None:
        with pyproject_path.open("rb") as handle:
            data = tomllib.load(handle)
    else:
        # Minimal parser fallback for py3.10
        current_section = None
        version_value = None
        with pyproject_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                stripped = line.strip()
                if stripped.startswith("[") and stripped.endswith("]"):
                    current_section = stripped.strip("[]")
                elif current_section == "project" and stripped.startswith("version"):
                    _, value = stripped.split("=", 1)
                    version_value = value.strip().strip('"').strip("'")
                    break
        if version_value is not None:
            return version_value
    if isinstance(data, dict):
        project = data.get("project", {})
        if isinstance(project, dict):
            version = project.get("version")
            if isinstance(version, str):
                return version
    return None


def get_version() -> str:
    try:
        return metadata.version("benchmark_utils")
    except metadata.PackageNotFoundError:
        return _read_version_from_pyproject() or "0.0.0"


__version__ = get_version()  # pragma: no cover
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_version.py::test_version_from_metadata -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/benchmark_utils/version.py tests/test_version.py
git commit -m "fix: derive version from package metadata"
```

---

### Task 2: Add fallback test for pyproject.toml

**Files:**
- Modify: `tests/test_version.py`

**Step 1: Write the failing test**

Add test that forces `PackageNotFoundError` and asserts fallback to the version in `pyproject.toml`:

```python
def test_version_from_pyproject(monkeypatch):
    def fake_version(_: str) -> str:
        raise metadata.PackageNotFoundError

    monkeypatch.setattr(metadata, "version", fake_version)
    importlib.reload(version_mod)
    assert version_mod.__version__ == "0.2.5b1"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_version.py::test_version_from_pyproject -v`  
Expected: FAIL until fallback is implemented.

**Step 3: Write minimal implementation**

If not already included in Task 1, ensure `_read_version_from_pyproject()` is implemented as above.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_version.py::test_version_from_pyproject -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add tests/test_version.py src/benchmark_utils/version.py
git commit -m "test: cover pyproject version fallback"
```

---

### Task 3: Run full test suite

**Files:**
- Test: `tests/`

**Step 1: Run tests**

Run: `pytest -v`  
Expected: PASS.

**Step 2: Commit (if any changes)**

```bash
git status
```

If clean, no commit required.

---
