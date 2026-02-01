# PR Review: Dynamic Version Resolution

**Commits Reviewed:** ecc995c, f760891
**Review Date:** 2026-02-01
**Reviewers:** code-reviewer, pr-test-analyzer, silent-failure-hunter agents

---

## Executive Summary

The implementation of dynamic version resolution has **6 Critical issues** and **7 Important issues** that need to be addressed before merging. The most significant concerns are:

1. **Missing `tomli` dependency** will cause runtime crashes on Python 3.10
2. **Silent failure pattern** - all errors return "0.0.0" without logging
3. **Overly broad exception handling** that masks programming errors

---

## Files Changed

- `src/benchmark_utils/version.py` - Dynamic version resolution implementation
- `tests/test_version.py` - New test file with 2 tests
- `docs/plans/2026-02-01-version-from-pyproject.md` - Plan documentation

---

## Critical Issues (6 found)

### 1. Missing tomli dependency for Python 3.10

**Agent:** code-reviewer
**File:** `pyproject.toml` (dependencies)
**Confidence:** 95
**Line:** N/A - dependency not added

**Issue:** The code attempts to import `tomli` as a fallback for Python 3.10, but `tomli` is not listed in `pyproject.toml` dependencies. The project specifies `requires-python = ">=3.10,<3.15"` and includes Python 3.10 support, but the fallback will fail on Python 3.10 systems without `tomli` installed.

**Fix:** Add conditional dependency to `pyproject.toml`:
```toml
dependencies = [
    "rich",
    "tomli>=2.0.0; python_version<'3.11'"
]
```

---

### 2. Overly broad `except Exception` masks errors

**Agent:** code-reviewer, silent-failure-hunter
**File:** `src/benchmark_utils/version.py:42`
**Confidence:** 90

**Issue:** `except Exception:` catches everything including `ImportError`, `AttributeError`, `TypeError`, `MemoryError`, `KeyboardInterrupt`, `SystemExit`, and any other unexpected exception. Programming errors like passing wrong argument types would be silently caught.

**Hidden Errors:**
- Programming errors (wrong argument types)
- System-level failures (memory errors)
- Interrupts during version lookup
- Import corruption issues

**Fix:**
```python
try:
    from importlib.metadata import version
    return version("benchmark_utils")
except importlib.metadata.PackageNotFoundError:
    return _read_version_from_pyproject()
```

---

### 3. Module import crash when tomli unavailable on Python 3.10

**Agent:** code-reviewer, silent-failure-hunter
**File:** `src/benchmark_utils/version.py:17-19`
**Confidence:** 85

**Issue:** When `tomllib` is not available (Python 3.10), the code attempts to import `tomli`. If `tomli` is not installed, an unhandled `ModuleNotFoundError` will crash the module import with a cryptic error message.

**User Impact:** Users on Python 3.10 who install the package without dev dependencies will see a raw `ModuleNotFoundError` that doesn't explain what to do.

**Fix:**
```python
try:
    import tomllib
except ModuleNotFoundError:
    try:
        import tomli as tomllib
    except ModuleNotFoundError:
        raise RuntimeError(
            "Cannot determine package version: benchmark_utils requires either "
            "Python 3.11+ (for built-in tomllib) or tomli installed. "
            "Install tomli with: pip install tomli"
        )
```

---

### 4. No test for missing pyproject.toml fallback

**Agent:** pr-test-analyzer
**File:** `tests/test_version.py` (missing test)
**Rating:** 9/10
**Lines:** 24-25

**Issue:** Lines 24-25 (the exception handler returning "0.0.0") are not tested. This code executes when `pyproject.toml` is missing, unreadable, or when file operations fail. This is the ultimate fallback and must work.

**What could break:**
- Development environments where `pyproject.toml` was accidentally deleted
- Docker containers where file mounting failed
- Corrupted filesystems
- Permission issues preventing file reads

**Test to add:**
```python
def test_version_fallback_to_zero_when_pyproject_missing(monkeypatch, tmp_path):
    """Test that version returns '0.0.0' when metadata unavailable and pyproject.toml missing"""

    def fake_version_raises(_: str) -> str:
        raise Exception("metadata unavailable")

    monkeypatch.setattr(metadata, "version", fake_version_raises)

    # Patch Path to point to non-existent directory
    import benchmark_utils.version as version_mod
    original_path = Path(version_mod.__file__).parent

    def mock_parent(self):
        return tmp_path  # Directory without pyproject.toml

    monkeypatch.setattr(Path, "parent", property(mock_parent))
    importlib.reload(version_mod)

    assert version_mod.__version__ == "0.0.0"
```

---

### 5. "0.0.0" fallback masks all errors silently

**Agent:** silent-failure-hunter
**File:** `src/benchmark_utils/version.py:25, 42`
**Severity:** CRITICAL

**Issue:** The function returns "0.0.0" as a fallback in multiple scenarios. This is misleading because:

1. "0.0.0" is a valid semantic version that means something specific (initial development)
2. Users might think they're running version 0.0.0 when they're actually in an error state
3. Code checking `if __version__ == "0.0.0"` can't distinguish between actual version 0.0.0 and error state
4. Errors in version detection propagate silently through the system

**User Impact:**
- Dependency resolution tools might treat "0.0.0" as a real version
- Bug reports will include incorrect version information
- Users can't detect when version resolution failed
- Downstream tools that rely on accurate versioning will malfunction

**Recommended Fix:** Use "UNKNOWN" sentinel and add warnings:
```python
import warnings

_VERSION_UNKNOWN = "UNKNOWN"

def _read_version_from_pyproject() -> str:
    try:
        # ... existing code ...
    except FileNotFoundError:
        warnings.warn(
            f"pyproject.toml not found at {pyproject_path}, "
            f"version will be reported as '{_VERSION_UNKNOWN}'"
        )
        return _VERSION_UNKNOWN
    except OSError as e:
        warnings.warn(
            f"Cannot read {pyproject_path}: {e}, "
            f"version will be reported as '{_VERSION_UNKNOWN}'"
        )
        return _VERSION_UNKNOWN
```

---

### 6. No test for Python 3.10 without tomli

**Agent:** pr-test-analyzer
**File:** `tests/test_version.py` (missing test)
**Rating:** 8/10
**Lines:** 17-19

**Issue:** When `tomllib` is not available (Python 3.10), the code attempts to import `tomli`. If `tomli` is not installed, an unhandled `ModuleNotFoundError` will crash the module import.

**Test to add:**
```python
def test_python_310_without_tomli_graceful_fallback(monkeypatch):
    """Test that Python 3.10 without tomli falls back to 0.0.0 rather than crashing"""

    def fake_version_raises(_: str) -> str:
        raise Exception("metadata unavailable")

    monkeypatch.setattr(metadata, "version", fake_version_raises)

    # Simulate both tomllib and tomli being unavailable
    import builtins
    original_import = builtins.__import__

    def mock_import(name, *args, **kwargs):
        if name in ('tomllib', 'tomli'):
            raise ModuleNotFoundError(f"No module named '{name}'")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, '__import__', mock_import)
    importlib.reload(version_mod)

    # Should fall back to 0.0.0 instead of crashing
    assert version_mod.__version__ == "0.0.0"
```

---

## Important Issues (7 found)

### 7. Path traversal assumes specific directory structure

**Agent:** code-reviewer
**File:** `src/benchmark_utils/version.py:12`
**Confidence:** 82

**Issue:** `Path(__file__).parent.parent.parent / "pyproject.toml"` assumes the package is installed as `src/benchmark_utils/`. This breaks if:
- The package is installed in editable mode with different structure
- The module is imported from a different location
- The code is run from a different working directory

**Fix:** Implement path search walking up directory tree:
```python
def _find_pyproject_toml() -> Path | None:
    """Find pyproject.toml by walking up the directory tree."""
    current = Path(__file__).resolve().parent
    for _ in range(5):  # Limit traversal depth
        if (current / "pyproject.toml").exists():
            return current / "pyproject.toml"
        if current.parent == current:  # Reached root
            break
        current = current.parent
    return None
```

---

### 8. No test for malformed pyproject.toml

**Agent:** pr-test-analyzer
**File:** `tests/test_version.py` (missing test)
**Rating:** 7/10
**Lines:** 21-23

**Issue:** The code catches `FileNotFoundError` and `OSError` but not `tomllib.TOMLDecodeError` (which occurs when the TOML file is malformed). A manually edited `pyproject.toml` with syntax errors will cause an unhandled exception.

**Test to add:**
```python
def test_malformed_pyproject_toml(monkeypatch, tmp_path):
    """Test fallback to 0.0.0 when pyproject.toml is malformed"""

    def fake_version_raises(_: str) -> str:
        raise Exception("metadata unavailable")

    monkeypatch.setattr(metadata, "version", fake_version_raises)

    # Create a malformed pyproject.toml
    bad_pyproject = tmp_path / "pyproject.toml"
    bad_pyproject.write_text("[project\nversion = '0.2.5b1'")  # Missing closing bracket

    # Patch the path resolution
    import benchmark_utils.version as version_mod

    def mock_parent(self):
        return tmp_path.parent

    monkeypatch.setattr(Path, "parent", property(mock_parent))
    importlib.reload(version_mod)

    assert version_mod.__version__ == "0.0.0"
```

---

### 9. Test reload pattern causes state pollution

**Agent:** code-reviewer
**File:** `tests/test_version.py:16, 27`
**Confidence:** 80

**Issue:** Using `importlib.reload()` in tests without cleanup can pollute module state across test runs. While tests are isolated within each function, the monkeypatch on `metadata.version` persists after the test completes.

**Fix:** Consider using a fixture with cleanup or test internal functions directly:
```python
def test_version_from_pyproject(monkeypatch, tmp_path):
    """Test fallback to pyproject.toml when metadata unavailable"""
    # Mock the version function to raise error
    def fake_version_raises(_: str) -> str:
        raise importlib.metadata.PackageNotFoundError("benchmark_utils")

    monkeypatch.setattr(
        "benchmark_utils.version.get_version",
        lambda: _read_version_from_pyproject()
    )
    # Or test _read_version_from_pyproject() directly with a mock pyproject.toml
```

---

### 10. Hardcoded version assertion creates brittleness

**Agent:** code-reviewer
**File:** `tests/test_version.py:29`
**Confidence:** 80

**Issue:** The test asserts `version_mod.__version__ == "0.2.5b1"`, which will break whenever the version in `pyproject.toml` changes. This creates maintenance overhead.

**Fix:** Read the version from `pyproject.toml` dynamically in the test:
```python
import tomllib
from pathlib import Path

def test_version_from_pyproject(monkeypatch):
    # Read expected version from actual pyproject.toml
    pyproject = Path(__file__).parent.parent.parent / "pyproject.toml"
    with open(pyproject, "rb") as f:
        expected_version = tomllib.load(f)["project"]["version"]

    # ... rest of test
    assert version_mod.__version__ == expected_version
```

---

### 11. Missing TOML parsing error context

**Agent:** silent-failure-hunter
**File:** `src/benchmark_utils/version.py:22`
**Severity:** HIGH

**Issue:** If `pyproject.toml` has malformed TOML, users get a raw `TOMLDecodeError` that doesn't mention which file failed to parse. Users might not realize `pyproject.toml` is the problem.

**Fix:** Wrap the TOML parsing to provide better context:
```python
try:
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)
except tomllib.TOMLDecodeError as e:
    raise RuntimeError(
        f"Failed to parse {pyproject_path}: {e}"
    ) from e
```

---

### 12. Silent file read failures (permissions, I/O errors)

**Agent:** silent-failure-hunter
**File:** `src/benchmark_utils/version.py:24`
**Severity:** CRITICAL

**Issue:** The catch block for `(FileNotFoundError, OSError)` silently returns "0.0.0" without logging. This swallows:
- `PermissionError` - User lacks read permissions
- `IsADirectoryError` - `pyproject.toml` is a directory, not a file
- Other `OSError` subclasses - disk I/O errors, network filesystem issues

**User Impact:**
- If `pyproject.toml` exists but is unreadable due to permissions, the error is silently ignored
- If the file path calculation is wrong, no error is raised
- Users get "0.0.0" when the file exists but can't be read, with no indication of the problem

**Fix:** Add warnings before falling back (see Issue #5 for full implementation).

---

### 13. No test for missing version field in pyproject.toml

**Agent:** pr-test-analyzer
**File:** `tests/test_version.py` (missing test)
**Rating:** 6/10
**Lines:** 23

**Issue:** The code uses `.get("project", {}).get("version", "0.0.0")` which handles this case, but it's not explicitly tested. Adding a test documents this behavior and prevents regression.

**Test to add:**
```python
def test_pyproject_without_version_field(monkeypatch, tmp_path):
    """Test that missing version field in pyproject.toml returns 0.0.0"""

    def fake_version_raises(_: str) -> str:
        raise Exception("metadata unavailable")

    monkeypatch.setattr(metadata, "version", fake_version_raises)

    # Create pyproject.toml without version field
    no_version_pyproject = tmp_path / "pyproject.toml"
    no_version_pyproject.write_text("[project]\nname = 'benchmark_utils'")

    import benchmark_utils.version as version_mod

    def mock_parent(self):
        return tmp_path.parent

    monkeypatch.setattr(Path, "parent", property(mock_parent))
    importlib.reload(version_mod)

    assert version_mod.__version__ == "0.0.0"
```

---

## Suggestions

### 14. Tests couple to implementation details

**Agent:** pr-test-analyzer
**Rating:** 4/10

**Observation:** The tests mock `importlib.metadata.version` directly, which is an implementation detail. If the implementation changes to use a different metadata source, the tests would fail even if behavior remains correct.

**Verdict:** Acceptable given the constraints, but document why mocking is necessary in test docstrings.

---

## Strengths

1. **Good test naming:** `test_version_from_metadata` and `test_version_from_pyproject` clearly describe what is being tested

2. **Docstrings present:** Each test has a clear docstring explaining its purpose

3. **Monkeypatch used correctly:** The tests properly use pytest's `monkeypatch` fixture for reversible mocking

4. **Tests the primary use case:** The happy path (metadata available) and primary fallback (`pyproject.toml`) are both covered

5. **Test isolation:** Each test independently sets up its mocking conditions

6. **Proper Python practices:** Type annotations, docstrings, and the `from __future__ import annotations` pattern used elsewhere in the codebase

---

## Recommended Action Plan

### Must Fix Before Merge

1. **Add tomli dependency** to `pyproject.toml`:
   ```toml
   dependencies = ["rich", "tomli>=2.0.0; python_version<'3.11'"]
   ```

2. **Fix exception handling** in `get_version()`:
   ```python
   except importlib.metadata.PackageNotFoundError:
       return _read_version_from_pyproject()
   ```

3. **Add error handling** for missing tomli on Python 3.10

4. **Add tests** for:
   - Missing `pyproject.toml` returning "0.0.0" or "UNKNOWN"
   - Python 3.10 without tomli

### Strongly Recommended

5. **Replace "0.0.0" with "UNKNOWN"** sentinel and add warnings

6. **Add test** for malformed `pyproject.toml`

7. **Improve error context** for TOML parsing failures

### Nice to Have

8. **Make tests less brittle** by reading version dynamically from `pyproject.toml`

9. **Implement robust path resolution** instead of hardcoded traversal

10. **Consider fixture-based approach** instead of `importlib.reload()`

---

## Verification Steps

After fixes, re-run:
```bash
# Run version tests
uv run pytest tests/test_version.py -v

# Run full test suite
uv run pytest -v

# Re-run PR review to verify issues are resolved
```

---

## Summary Table

| # | Issue | Severity | Agent | File | Line |
|---|-------|----------|-------|------|------|
| 1 | Missing tomli dependency | CRITICAL | code-reviewer | pyproject.toml | N/A |
| 2 | Overly broad except Exception | CRITICAL | code-reviewer, silent-failure-hunter | version.py | 42 |
| 3 | Module import crash Python 3.10 | CRITICAL | code-reviewer, silent-failure-hunter | version.py | 17-19 |
| 4 | No test for missing pyproject.toml | CRITICAL | pr-test-analyzer | test_version.py | N/A |
| 5 | "0.0.0" fallback masks errors | CRITICAL | silent-failure-hunter | version.py | 25, 42 |
| 6 | No test for Python 3.10 without tomli | CRITICAL | pr-test-analyzer | test_version.py | N/A |
| 7 | Path traversal assumes structure | IMPORTANT | code-reviewer | version.py | 12 |
| 8 | No test for malformed TOML | IMPORTANT | pr-test-analyzer | test_version.py | N/A |
| 9 | Test reload state pollution | IMPORTANT | code-reviewer | test_version.py | 16, 27 |
| 10 | Hardcoded version assertion | IMPORTANT | code-reviewer | test_version.py | 29 |
| 11 | Missing TOML error context | HIGH | silent-failure-hunter | version.py | 22 |
| 12 | Silent file read failures | CRITICAL | silent-failure-hunter | version.py | 24 |
| 13 | No test for missing version field | IMPORTANT | pr-test-analyzer | test_version.py | N/A |
| 14 | Tests couple to implementation | SUGGESTION | pr-test-analyzer | test_version.py | - |

**Total Issues Found:** 14 (6 Critical, 7 Important, 1 Suggestion)
