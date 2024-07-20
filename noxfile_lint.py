import nox

locations = "."


@nox.session(python=["3.8", "3.9", "3.10", "3.11", "3.12"], venv_backend="uv")
def lint_ruff(session):
    args = session.posargs or locations
    session.install("ruff")
    session.run("ruff", "check", *args)
