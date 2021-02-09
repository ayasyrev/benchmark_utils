import nox

# from benchmark_utils.image_libs import image_packages_to_lib
# img_packages = list(image_packages_to_lib.keys())
from benchmark_utils.image_libs import image_libs_supported
pip_img_packages = [lib_name for lib_name in image_libs_supported
                    if image_libs_supported[lib_name].installation_type == 'pip']


@nox.session(python=["3.8"])
# @nox.parametrize('img_lib', ['pillow-simd', 'opencv-python-headless', 'jpeg4py', 'pyvips', 'scikit-image', 'imageio'])
@nox.parametrize('img_lib', pip_img_packages)
def tests(session, img_lib):
    args = session.posargs or ["--cov"]
    # args = session.posargs or ['']
    session.install(".", "pytest", "pytest-cov", "coverage[toml]")
    # session.install(".", "pytest")
    session.install(image_libs_supported[img_lib].package)
    # session.run("pytest", external=True)
    # session.run("pytest", '--img_lib', image_packages_to_lib[img_lib], *args)
    # session.run("pytest", '--img_lib', image_libs_supported[img_lib].import_name, *args)
    session.run("pytest", '--img_lib', img_lib, *args)


# locations = "benchmark_utils", "tests", "noxfile.py"


# @nox.session(python=["3.8", "3.7", "3.9"])
# def lint(session):
#     args = session.posargs or locations
#     session.install("flake8", "flake8-import-order")
#     session.run("flake8", *args)
