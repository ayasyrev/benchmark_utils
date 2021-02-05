import nox


@nox.session(python=["3.8", "3.7", "3.9"])
def tests(session):
    session.install(".", "pytest")
    session.run("pytest", external=True)


locations = "tests", "noxfile.py"


@nox.session(python=["3.8", "3.7", "3.9"])
def lint(session):
    args = session.posargs or locations
    session.install("flake8")
    session.run("flake8", *args)
