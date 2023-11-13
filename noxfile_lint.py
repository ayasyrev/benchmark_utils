import nox


locations = "src/benchmark_utils", "tests", "noxfile.py"


@nox.session(python=["3.8", "3.9", "3.10", "3.11", 3.12])
def lint(session):
    args = session.posargs or locations
    session.install("flake8")
    session.run("flake8", *args)
