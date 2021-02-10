import importlib
from abc import ABC

from benchmark_utils.image_libs import image_libs_supported, ImageLibCfg
from benchmark_utils.image_libs.read_image import image_read_dict

image_lib_available = [lib_name for lib_name in image_libs_supported if importlib.util.find_spec(lib_name) is not None]


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
