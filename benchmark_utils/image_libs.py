import importlib
from abc import ABC
from typing import Union, List

# from importlib.metadata import version
# import sys
# import pkg_resources

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


class ImageLib(ABC):
    __version__: str = ''
    installation_type: str = ''
    package: Union[str, List[str]] = ''

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return f"{self.__class__.__name__}: pkg: {self.package}, ver: {self.__version__}"

    def read(self, file_name: str) -> object:
        raise NotImplementedError


class ImageLibPIL(ImageLib):
    def __init__(self) -> None:
        super().__init__()
        if 'PIL' in image_lib_available:
            from PIL import __version__, Image
            self.__version__ = __version__
            self.image_open = Image.open
        else:
            self.__version__ = ''

        self.installation_type = 'pip'
        self.package = 'pillow'

    def read(self, file_name: str) -> object:
        with open(file_name, 'rb') as file:
            img = self.image_open(file)
            return img.convert('RGB')


image_libs_dict = {'PIL': ImageLibPIL}


class ImageLibs:
    def __init__(self) -> None:
        self.supported = ["torchvision", "PIL", "cv2", "jpeg4py", "accimage", "pyvips", "skimage", "imageio"]
        self.available = [library for library in self.supported if importlib.util.find_spec(library) is not None]
        # self.lib_versions = {lib_name: version(lib_name) for lib_name in self.available}
        self._libs = {lib_name: image_libs_dict[lib_name]() for lib_name in self.available
                      if lib_name in image_libs_dict}

    def __getitem__(self, lib_name):
        return self._libs[lib_name]

    def __repr__(self) -> str:
        return f"Image Libs: {', '.join(self.available)}"
