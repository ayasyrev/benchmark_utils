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
