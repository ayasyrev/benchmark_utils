import nox


@nox.session(python=["3.8", "3.7", "3.9"])
def tests(session):
    # session.install("poetry", "pytest")
    session.install(".", "pytest")
    # session.run("poetry", "install", external=True)
    session.run("pytest", external=True)


locations = "src", "tests", "noxfile.py"


@nox.session(python=["3.8", "3.7", "3.9"])
def lint(session):
    args = session.posargs or locations
    session.install("flake8")
    session.run("flake8", *args)
