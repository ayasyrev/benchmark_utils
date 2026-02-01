# UV Migration Inventory - 2026-02-01

## Purpose
Detailed inventory of current metadata, dependencies, and configuration for migration to uv-build packaging and Python 3.10-3.14 support.

## 1. File Contents

### pyproject.toml
```toml
[tool.ruff]
# Assume Python 3.8
target-version = "py38"
```

### setup.cfg
```ini
[metadata]
name = benchmark_utils
version = attr: benchmark_utils.version.__version__
author = Yasyrev Andrei
author_email = a.yasyrev@gmail.com
description = Utils for benchmark.
long_description = file: README.md
long_description_content_type = text/markdown
url = https://github.com/ayasyrev/benchmark_utils
license = apache2
classifiers =
    Programming Language :: Python :: 3.8
    Programming Language :: Python :: 3.9
    Programming Language :: Python :: 3.10
    Programming Language :: Python :: 3.11
    Programming Language :: Python :: 3.12
    License :: OSI Approved :: Apache Software License
    Operating System :: OS Independent

[options]
package_dir =
    = src
packages = find:

[options.packages.find]
where = src
```

### setup.py
```python
from setuptools import setup

REQUIREMENTS_FILENAME = "requirements.txt"
REQUIREMENTS_TEST_FILENAME = "requirements_test.txt"
REQUIREMENTS_DEV_FILENAME = "requirements_dev.txt"

def load_requirements(filename: str) -> list[str]:
    """Load requirements from file"""
    try:
        with open(filename, encoding="utf-8") as fh:
            return fh.read().splitlines()
    except FileNotFoundError:
        return []

REQUIRED = load_requirements(REQUIREMENTS_FILENAME)
TEST_REQUIRED = load_requirements(REQUIREMENTS_TEST_FILENAME)
DEV_REQUIRED = load_requirements(REQUIREMENTS_DEV_FILENAME)

EXTRAS = {
    "test": TEST_REQUIRED,
    "dev": DEV_REQUIRED + TEST_REQUIRED,
}

setup(
    install_requires=REQUIRED,
    extras_require=EXTRAS,
)
```

### requirements.txt
```
rich
```

### requirements_dev.txt
```
black
black[jupyter]
coverage[toml]
flake8
isort
mypy
nbmetaclean
nox
pre-commit
ruff
```

### requirements_test.txt
```
pytest
pytest-cov
```

### .github/workflows/tests.yml
```yaml
name: Tests
on:
  push:
    branches:
      - dev
      - main
jobs:
  tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python: ["3.8", "3.9", "3.10", "3.11", "3.12"]
    steps:
    - name: Checkout
      uses: actions/checkout@main
    - name: Setup Python ${{ matrix.python }}
      uses: actions/setup-python@main
      with:
        python-version: ${{ matrix.python }}
        architecture: x64

    - name: Install
      run: |
        pip install uv
        uv pip install --system .[test] "coverage[toml]"
    - name: Tests
      run: pytest --cov

    - name: Coverage
      if: ${{ matrix.python == '3.11' }}
      uses: codecov/codecov-action@main
      with:
        token: ${{ secrets.CODECOV_TOKEN }}
        slug: ayasyrev/benchmark_utils
```

### .github/workflows/lint.yml
```yaml
name: Lint
on:
  push:
    branches:
      - dev
      - main
jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@main
    - uses: actions/setup-python@main
      with:
        python-version: "3.11"
        architecture: x64
    - run: pip install ruff
    - run: ruff check .
```

### .github/workflows/deploy_docs.yml
```yaml
name: Deploy_docs
on:
  push:
    branches:
      - main
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@main
      - uses: actions/setup-python@main
        with:
          python-version: 3.x
      - run: pip install mkdocs-material
      - run: pip install pymdown-extensions
      - run: mkdocs gh-deploy --force
```

### noxfile.py
```python
import nox

@nox.session(python=["3.8", "3.9", "3.10", "3.11", "3.12"], venv_backend="uv")
def tests(session):
    args = session.posargs or ["--cov"]
    session.install("-e .[test]")
    session.run("pytest", *args)
```

### noxfile_lint.py
```python
import nox

locations = "."

@nox.session(python=["3.8", "3.9", "3.10", "3.11", "3.12"], venv_backend="uv")
def lint_ruff(session):
    args = session.posargs or locations
    session.install("ruff")
    session.run("ruff", "check", *args)
```

### noxfile_cov.py
```python
import nox

@nox.session(python=["3.11"], venv_backend="uv")
def tests_cov(session):
    args = session.posargs or ["--cov"]
    session.install("-e .[test]", "coverage[toml]")
    session.run("pytest", *args)


@nox.session(python="3.11", venv_backend="uv")
def coverage(session) -> None:
    """Upload coverage data."""
    session.install("coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
```

### README.md
```markdown
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/benchmark-utils)](https://pypi.org/project/benchmark-utils/)
...
Tested on python 3.8 - 3.12
```

## 2. Current Python Support Summary

| Location | Current Version(s) |
|----------|-------------------|
| pyproject.toml - ruff target-version | py38 |
| setup.cfg - classifiers | 3.8, 3.9, 3.10, 3.11, 3.12 |
| .github/workflows/tests.yml - matrix | 3.8, 3.9, 3.10, 3.11, 3.12 |
| .github/workflows/lint.yml - python-version | 3.11 |
| .github/workflows/deploy_docs.yml - python-version | 3.x (latest) |
| noxfile.py - sessions | 3.8, 3.9, 3.10, 3.11, 3.12 |
| noxfile_lint.py - sessions | 3.8, 3.9, 3.10, 3.11, 3.12 |
| noxfile_cov.py - sessions | 3.11 |
| README.md - support statement | 3.8 - 3.12 |

**Target after migration:** 3.10, 3.11, 3.12, 3.13, 3.14

## 3. Current Dependencies Summary

### Main Dependencies
- `rich`

### Test Dependencies
- `pytest`
- `pytest-cov`

### Dev Dependencies
- `black`
- `black[jupyter]`
- `coverage[toml]`
- `flake8`
- `isort`
- `mypy`
- `nbmetaclean`
- `nox`
- `pre-commit`
- `ruff`

### Extras Groups
- `test` - includes test dependencies
- `dev` - includes dev + test dependencies

## 4. UV Usage Confirmation

✅ **UV is already used in the following locations:**

1. **noxfile.py** - `venv_backend="uv"` parameter on test sessions
2. **noxfile_lint.py** - `venv_backend="uv"` parameter on lint sessions
3. **noxfile_cov.py** - `venv_backend="uv"` parameter on coverage sessions
4. **.github/workflows/tests.yml** - `pip install uv` followed by `uv pip install --system .[test] "coverage[toml]"`

**Conclusion:** Project already uses uv for local development (nox) and CI testing. Only packaging metadata migration remains.

## 5. Files to Remove After Migration

### setup.cfg
**Rationale:** Superseded by pyproject.toml [project] section in uv-build. All metadata (name, version, author, classifiers, etc.) will be moved to pyproject.toml.

### setup.py
**Rationale:** Superseded by pyproject.toml [project] and [project.optional-dependencies] sections. Dynamic requirement loading will be replaced with static dependency declarations in pyproject.toml.

### requirements.txt
**Rationale:** Main dependencies will be moved to pyproject.toml [project.dependencies].

### requirements_dev.txt
**Rationale:** Dev dependencies will be moved to pyproject.toml [project.optional-dependencies] under the "dev" extra.

### requirements_test.txt
**Rationale:** Test dependencies will be moved to pyproject.toml [project.optional-dependencies] under the "test" extra.

**Migration approach:**
1. Consolidate all dependencies into pyproject.toml
2. Create uv.lock with `uv lock`
3. Verify CI and nox work with new configuration
4. Remove legacy files (setup.cfg, setup.py, requirements*.txt)
5. Update Python version declarations from 3.8-3.12 to 3.10-3.14

## 6. Migration Task Checklist

- [ ] Update pyproject.toml with [project] section
- [ ] Move dependencies to pyproject.toml
- [ ] Update Python version declarations to 3.10-3.14
- [ ] Run `uv lock` to generate lockfile
- [ ] Update CI workflows to use 3.10-3.14 matrix
- [ ] Update nox sessions to use 3.10-3.14
- [ ] Update README.md support statement
- [ ] Test locally with nox
- [ ] Verify CI passes
- [ ] Remove setup.cfg, setup.py, requirements*.txt
- [ ] Commit changes
