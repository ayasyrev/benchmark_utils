import importlib
from dataclasses import dataclass
from abc import ABC
# from typing import List

from benchmark_utils.read_image import image_read_dict

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


@dataclass
class ImageLibCfg:
    lib_name: str
    package: str
    # import_name: str
    installation_type: str = 'pip'


image_libs_supported = {"torchvision": ImageLibCfg('torchvision', 'torchvision'),
                        # "pillow-simd": ImageLibCfg('PIL-simd', 'pillow-simd', 'PIL'),
                        "PIL": ImageLibCfg('PIL', 'pillow'),
                        # "opencv": ImageLibCfg('opencv', 'opencv-python', 'cv2'),
                        # "opencv-headless": ImageLibCfg('opencv-headless', 'opencv-python-headless', 'cv2'),
                        "cv2": ImageLibCfg('cv2', 'opencv-python-headless'),
                        "jpeg4py": ImageLibCfg('jpeg4py', 'jpeg4py'),
                        "accimage": ImageLibCfg('accimage', 'accimage', installation_type='conda'),
                        "pyvips": ImageLibCfg('pyvips', 'pyvips'),
                        "skimage": ImageLibCfg('skimage', 'skimage'),
                        "imageio": ImageLibCfg('imageio', 'imageio')}


class ImageLib(ABC):
    def __init__(self, image_lib: ImageLibCfg, read_func: callable = None, version: str = '') -> None:
        super().__init__()
        self.lib_name = image_lib.lib_name
        self.installation_type: str = image_lib.installation_type
        self.package: str = image_lib.package
        if read_func is None:
            self._read_func = image_read_dict[self.lib_name]['read_func']
            self.__version__ = image_read_dict[self.lib_name]['version']
        else:
            self._read_func: callable = read_func
            self.__version__ = version

    def __str__(self):
        return self.lib_name

    def __repr__(self):
        return f"{self.lib_name}: pkg: {self.package}, ver: {self.__version__}"

    def read(self, file_name: str) -> object:
        return self._read_func(file_name)


# if 'PIL' in image_lib_available:
#     image_libs_dict['PIL'] = ImageLib(image_libs_supported['pillow'])


class ImageLibs:
    def __init__(self) -> None:
        self.supported = [lib_name for lib_name in image_libs_supported]
        self.available = [lib_name for lib_name in self.supported
                          if importlib.util.find_spec(lib_name) is not None]
        # self._libs = {lib_name: image_libs_dict[lib_name] for lib_name in self.available
        #               if lib_name in image_libs_dict}
        self._libs = {lib_name: ImageLib(image_libs_supported[lib_name]) for lib_name in self.available
                      if lib_name in image_read_dict}

    def __getitem__(self, lib_name):
        return self._libs[lib_name]

    def __repr__(self) -> str:
        return f"Image Libs: {', '.join(self.available)}"
