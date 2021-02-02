import nox
from nox.sessions import Session
from typing import Any


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    ...


@nox.session(python=["3.8"])
def tests(session):
    session.run("poetry", "install", external=True)
    # session.run("pytest", external=True)


locations = "src", "tests", "noxfile.py"


@nox.session(python=["3.8"])
def lint(session):
    args = session.posargs or locations
    session.install("flake8")
    session.run("flake8", *args)


# @nox.session(python=["3.8"])
# def mypy(session):
#     session.install("mypy")
#     args = session.posargs or locations
#     install_with_constraints(session, "mypy")
#     session.run("mypy", *args)

@nox.session(python="3.8")
def coverage(session: Session) -> None:
    """Upload coverage data."""
    session.install("coverage", "coverage[toml]", "codecov")
    # install_with_constraints(session, "coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
