import nox

locations = "src/benchmark_utils", "tests", "noxfile.py"


@nox.session(python=["3.8", "3.9", "3.7", "3.10"], venv_backend="mamba")
def lint(session):
    args = session.posargs or locations

    session.conda_install("flake8")
    session.run("flake8", *args)