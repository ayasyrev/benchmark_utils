# UV Migration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Migrate packaging and tooling to uv, and set Python support to 3.10–3.14.

**Architecture:** Use PEP 621 metadata in `pyproject.toml` with `uv-build` backend, and move dependency declarations into `[project]` and extras. Replace legacy config/requirements files and update automation to use uv.

**Tech Stack:** Python, uv, uv-build (PEP 517), nox, pytest, ruff, GitHub Actions.

---

### Task 1: Inventory current metadata and dependencies
**Files:**
- Read: `pyproject.toml`
- Read: `setup.cfg`
- Read: `setup.py`
- Read: `requirements.txt`
- Read: `requirements_dev.txt`
- Read: `requirements_test.txt`
- Read: `.github/workflows/tests.yml`
- Read: `.github/workflows/lint.yml`
- Read: `.github/workflows/deploy_docs.yml`
- Read: `noxfile.py`
- Read: `noxfile_lint.py`
- Read: `noxfile_cov.py`
- Read: `README.md`

**Step 1: Record current Python versions and deps**
- Note current `ruff` target-version, classifiers, test matrix, nox sessions, and README support claims.
- Confirm uv usage in CI and nox.

**Step 2: Decide removals**
- Default: remove `setup.cfg`, `setup.py`, `requirements*.txt` after moving content to `pyproject.toml` and `uv.lock`.

### Task 2: Update `pyproject.toml` for uv-build + PEP 621
**Files:**
- Modify: `pyproject.toml`

**Step 1: Add PEP 621 metadata**
- Add `[build-system]` with `build-backend = "uv_build"` and `requires = ["uv-build"]`.
- Add `[project]` with name, version (existing attr), description, readme, license, authors, urls.
- Add `requires-python = ">=3.10,<3.15"`.
- Add classifiers for 3.10–3.14.

**Step 2: Move dependencies**
- `[project.dependencies]` contains `rich`.
- `[project.optional-dependencies]`:
  - `test = ["pytest", "pytest-cov"]`
  - `dev = ["black", "black[jupyter]", "coverage[toml]", "flake8", "isort", "mypy", "nbmetaclean", "nox", "pre-commit", "ruff"]`

**Step 3: Update ruff target**
- Set `target-version = "py310"`.

### Task 3: Remove legacy packaging files
**Files:**
- Delete: `setup.cfg`
- Delete: `setup.py`
- Delete: `requirements.txt`
- Delete: `requirements_dev.txt`
- Delete: `requirements_test.txt`

**Step 1: Remove files after `pyproject.toml` is complete**
- Ensure no tooling still references these files.

### Task 4: Update nox sessions for Python 3.10–3.14
**Files:**
- Modify: `noxfile.py`
- Modify: `noxfile_lint.py`
- Modify: `noxfile_cov.py`

**Step 1: Update version lists**
- Replace 3.8/3.9 with 3.10–3.14 in `python=[...]`.
- Keep coverage session pinned to a single version (recommend 3.12 or 3.13).

### Task 5: Update GitHub Actions CI
**Files:**
- Modify: `.github/workflows/tests.yml`
- Modify: `.github/workflows/lint.yml`
- Modify: `.github/workflows/deploy_docs.yml`

**Step 1: Tests matrix**
- Set matrix to `["3.10", "3.11", "3.12", "3.13", "3.14"]`.

**Step 2: Lint**
- Use a stable single version (3.12 or 3.13).

**Step 3: Docs**
- Pin to a stable single version (3.12 or 3.13).

**Step 4: uv install**
- Prefer `uv pip install --system .[test]` or `uv sync --extra test` (align with chosen workflow).

### Task 6: Update README and badges
**Files:**
- Modify: `README.md`

**Step 1: Update support statement**
- Replace "Tested on python 3.8 - 3.12" with "Tested on python 3.10 - 3.14".

**Step 2: Install instructions**
- Add uv-based install snippet (e.g., `uv pip install -e .[test]`).

### Task 7: Generate uv lockfile
**Files:**
- Create: `uv.lock`

**Step 1: Sync**
- Run `uv sync --extra test` to generate `uv.lock`.
- Ensure lock captures extras.

### Task 8: Verification
**Step 1: Lint**
- Run `ruff check .`.

**Step 2: Tests**
- Run `pytest --cov` (or via nox on one version).

**Step 3: Build metadata**
- Run `uv build` (or `python -m build` if needed) and confirm success.

### Task 9: Cleanup and commit
**Step 1: Review git status**
- Ensure only expected files changed.

**Step 2: Commit**
- Commit message example: `chore: migrate packaging to uv-build and update python support`.

---

**Open decisions (defaults proposed):**
- **Coverage/lint Python version:** default to 3.12 (stable).
- **Keep `requirements*.txt` as exports?** default: remove entirely.
