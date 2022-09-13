import nox


@nox.session(python=["3.8", "3.9", "3.7", "3.10"], venv_backend='mamba')
def tests(session):
    args = session.posargs or ["--cov"]
    session.conda_install('--file', 'requirements_test.txt')
    # session.install('.', '--no-deps')
    session.install('.')
    # session.install(".", "pytest", "pytest-cov", "coverage[toml]")
    session.run("pytest", *args)