import nox


locations = "src/benchmark_utils", "tests", "noxfile.py"


@nox.session(python=["3.6", "3.7", "3.8", "3.9", "3.10", "3.11"])
def lint(session):
    args = session.posargs or locations
    session.install("flake8")
    session.run("flake8", *args)
