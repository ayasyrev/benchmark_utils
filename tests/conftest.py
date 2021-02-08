
def pytest_addoption(parser):
    parser.addoption(
        "--img_lib",
        action="append",
        default=[],
        help="list of stringinputs to pass to test functions",
    )


def pytest_generate_tests(metafunc):
    if "img_lib" in metafunc.fixturenames:
        metafunc.parametrize("img_lib", metafunc.config.getoption("img_lib"))
