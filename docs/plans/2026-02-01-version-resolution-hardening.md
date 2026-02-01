# Version Resolution Hardening Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make version resolution robust across Python 3.10–3.14 with clear warnings on failures, correct dependency handling, and comprehensive tests.

**Architecture:** Keep `get_version()` as the entry point. Use `importlib.metadata.version` first; on `PackageNotFoundError`, fall back to `_read_version_from_pyproject()`. Introduce `_VERSION_UNKNOWN = "UNKNOWN"` and emit warnings for missing/invalid TOML or IO errors. Add `_find_pyproject_toml()` for robust path lookup and `_load_tomllib()` for tomllib/tomli availability.

**Tech Stack:** Python 3.10+, pytest, importlib.metadata, tomllib/tomli, warnings.

---

### Task 0: Prep worktree (required)
**Files:** none
**Step 1: Create isolated worktree**
Run: `@using-git-worktrees`
Expected: new worktree ready for edits.

---

### Task 1: Add conditional tomli dependency
**Files:**
- Modify: `pyproject.toml`

**Step 1: Update dependencies**
Set:
```toml
dependencies = [
    "rich",
    "tomli>=2.0.0; python_version<'3.11'"
]
```

**Step 2: Verify pyproject parses**
Run: `python -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"`
Expected: exit code 0

**Step 3: Commit**
```bash
git add pyproject.toml
git commit -m "chore: add tomli fallback for py310"
```

---

### Task 2: Harden version resolution logic
**Files:**
- Modify: `src/benchmark_utils/version.py`

**Step 1: Write failing tests (stubs)**
Add placeholders in `tests/test_version.py` for:
- missing pyproject -> UNKNOWN + warning
- malformed TOML -> UNKNOWN + warning
- missing tomllib/tomli -> UNKNOWN + warning
- missing version field -> UNKNOWN + warning
- metadata available -> metadata value
- metadata missing -> pyproject value

**Step 2: Run tests to confirm failures**
Run: `uv run pytest tests/test_version.py -v`
Expected: FAILs

**Step 3: Implement minimal code changes**
Add:
- `_VERSION_UNKNOWN = "UNKNOWN"`
- `_load_tomllib()` to handle tomllib/tomli missing with warnings
- `_find_pyproject_toml()` walking up directories (depth-limited)
- `_read_version_from_pyproject()` that:
  - warns on missing pyproject
  - warns on IO errors
  - warns on TOML decode errors
  - warns on missing `[project].version`
  - returns `_VERSION_UNKNOWN` in all warning cases
- Narrow `get_version()` except to `importlib.metadata.PackageNotFoundError`

**Step 4: Run targeted tests**
Run: `uv run pytest tests/test_version.py -v`
Expected: PASS

**Step 5: Commit**
```bash
git add src/benchmark_utils/version.py
git commit -m "fix: harden version resolution and warnings"
```

---

### Task 3: Update and expand tests
**Files:**
- Modify: `tests/test_version.py`

**Step 1: Avoid reload-based tests**
Call `version_mod.get_version()` directly instead of reloading and reading `__version__`.

**Step 2: Implement tests**
- Metadata success path
- Metadata missing -> pyproject value (read from real `pyproject.toml`)
- Missing pyproject -> UNKNOWN + warning
- Missing tomllib/tomli -> UNKNOWN + warning
- Malformed TOML -> UNKNOWN + warning
- Missing version field -> UNKNOWN + warning

**Step 3: Run tests**
Run: `uv run pytest tests/test_version.py -v`
Expected: PASS

**Step 4: Commit**
```bash
git add tests/test_version.py
git commit -m "test: cover version fallbacks and warnings"
```

---

### Task 4: Full verification
**Files:** none

**Step 1: Run full suite**
Run: `uv run pytest -v`
Expected: PASS

**Step 2: Commit**
Only if additional fixes required.

---
