import nox

# from benchmark_utils.image_libs import image_libs_supported

# conda_img_packages = [lib_name for lib_name in image_libs_supported
#                       if image_libs_supported[lib_name].installation_type == 'conda']
conda_img_packages = ['accimage', 'pyvips']


@nox.session(python=["3.8", "3.9"], venv_backend='conda')
@nox.parametrize('img_lib', conda_img_packages)
def tests_conda(session, img_lib):
    args = session.posargs or ["--cov"]
    session.install(".", "pytest", "pytest-cov", "coverage[toml]")
    session.conda_install(img_lib, '--channel=conda-forge')
    session.conda_install('numpy')
    # session.install(image_libs_supported[img_lib].package)
    session.run("pytest", '--img_lib', img_lib, *args)
