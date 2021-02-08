import importlib
# from importlib.metadata import version
# import sys

# import pkg_resources

ACCIMAGE_AVAILABLE = importlib.util.find_spec("accimage") is not None
CV2_AVAILABLE = importlib.util.find_spec("cv2") is not None
IMAGEIO_AVAILABLE = importlib.util.find_spec("imageio") is not None
PYVIPS_AVAILABLE = importlib.util.find_spec("pyvips") is not None
SKIMAGE_AVAILABLE = importlib.util.find_spec("skimage") is not None
JPEG4PY_AVAILABLE = importlib.util.find_spec("jpeg4py") is not None
PIL_AVAILABLE = importlib.util.find_spec("PIL") is not None
TORCHVISION_AVAILABLE = importlib.util.find_spec("torchvision") is not None


# if TORCHVISION_AVAILABLE:
#     tv_version = version('torchvision')
#     print(tv_version)
# else:
#     print('TV unavailable')
# def print_package_versions(packages: List[str]) -> None:
#     package_versions = {"python": sys.version}
#     for package in packages:
#         try:
#             package_versions[package] = pkg_resources.get_distribution(package).version
#         except pkg_resources.DistributionNotFound:
#             pass
#     print(package_versions)

image_packages_to_lib = {"torchvision": 'torchvision',
                         "pillow-simd": 'PIL',
                         "pillow": 'PIL',
                         "opencv-python": 'cv2',
                         "opencv-python-headless": 'cv2',
                         "jpeg4py": 'jpeg4py',
                         "accimage": 'accimage',
                         "pyvips": 'pyvips',
                         "scikit-image": 'skimage',
                         "imageio": 'imageio'}
packages  = ["torchvision", "pillow-simd", "pillow", "opencv-python", "jpeg4py", "accimage", "pyvips", "scikit-image", "imageio"]  # noqa E501, E221
libraries = ["torchvision", "PIL",                   "cv2",           "jpeg4py", "accimage", "pyvips", "skimage",      "imageio"]  # noqa E501
image_lib_available = [library for library in libraries if importlib.util.find_spec(library) is not None]
if "torchvision" in image_lib_available:
    if not TORCHVISION_AVAILABLE:
        image_lib_available.pop(image_lib_available.index('torchvision'))


class ImageLibs:
    def __init__(self) -> None:
        self.supported = ["torchvision", "PIL", "cv2", "jpeg4py", "accimage", "pyvips", "skimage", "imageio"]
        self.available = [library for library in self.supported if importlib.util.find_spec(library) is not None]
        # self.lib_versions = {lib_name: version(lib_name) for lib_name in self.available}

    def __repr__(self) -> str:
        return f"Image Libs: {', '.join(self.available)}"


img_libs = ImageLibs()
print(img_libs)
# print(img_libs.lib_versions)
