import nox


@nox.session(python=["3.8", "3.9", "3.10", "3.11"])
def tests(session):
    args = session.posargs or ["--cov"]
    session.install(".", "pytest", "pytest-cov", "coverage[toml]")
    session.run("pytest", *args)
