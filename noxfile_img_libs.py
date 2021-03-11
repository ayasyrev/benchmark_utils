import nox

# from benchmark_utils.image_libs import image_libs_supported
# pip_img_packages = [lib_name for lib_name in image_libs_supported
#                     if image_libs_supported[lib_name].installation_type == 'pip']
pip_img_packages = ['torchvision', 'PIL', 'cv2', 'skimage', 'imageio']  # 'jpeg4py', 'pyvips'
lib_to_package = {
    'torchvision': 'torchvision',
    'PIL': 'pillow',
    'cv2': 'opencv-python-headless',
    'jpeg4py': 'jpeg4py',
    'skimage': 'scikit-image',
    'imageio': 'imageio',
    'pyvips': 'pyvips'}


@nox.session(python=["3.8", "3.9", "3.7"])
@nox.parametrize('img_lib', pip_img_packages)
def tests(session, img_lib):
    args = session.posargs or ["--cov"]
    session.install(".", "pytest", "pytest-cov", "coverage[toml]")
    session.install(lib_to_package[img_lib])
    if img_lib == 'pyvips':
        session.install('numpy')
    session.run("pytest", '--img_lib', img_lib, *args)
