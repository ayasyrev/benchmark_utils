import nox

from benchmark_utils.image_libs_supported import image_libs_supported
pip_img_packages = [lib_name for lib_name in image_libs_supported
                    if image_libs_supported[lib_name].installation_type == 'pip']


@nox.session(python=["3.8"])
@nox.parametrize('img_lib', pip_img_packages)
def tests(session, img_lib):
    args = session.posargs or ["--cov"]
    session.install(".", "pytest", "pytest-cov", "coverage[toml]")
    session.install(image_libs_supported[img_lib].package)
    session.run("pytest", '--img_lib', img_lib, *args)
