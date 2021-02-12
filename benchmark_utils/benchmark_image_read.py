from .benchmark import BenchmarkIter
# , benchmark_bar_persec
# from .image_libs import image_libs_supported
from .image_libs.image_libs import ImageLibs
from .image_libs.get_image_files import get_img_filenames
# from .image_libs.read_image import image_read_dict

# _img_to_nparray, get_img_filenames
from typing import Dict, Union


class BenchmarkImageRead(BenchmarkIter):
    """Benchmark for read images.
    """
    def __init__(self,
                 func: Union[Dict[str, callable], None] = None,
                 data_dir: str = None,
                 num_images: int = 2000,
                 num_repeats: int = 5):
        """Benchmark Image Read funcs.

        Args:
            func (Dict[str, callable], optional): Dictionary with func to read images. Defaults to read_img_to_nparray.
            data_dir (str): Directory with images.
            num_images (int, optional): How many images take for test. Defaults to 2000, 0 - use all images.
            num_repeats (int, optional): Repeat test for num_repeats times. Defaults to 5.
        """
        if func is None:
            image_libs = ImageLibs()
            bench_func_dict = {image_lib: image_libs[image_lib]._read_func for image_lib in image_libs.available}
        else:
            bench_func_dict = func
        # bench_func_dict = {}
        # for image_lib in image_libs.available:
        #     function = func.get(image_lib)
        #     if function is not None:
        #         image_libs.append(image_lib)
        #         bench_func_dict[image_lib] = function
        super().__init__(func=bench_func_dict, num_repeats=num_repeats)

        self.image_libs = image_libs
        self._num_items = None
        self.data_dir = data_dir
        self.num_items = num_images
        # self._benchmark = benchmark_bar_persec
        self.results_header = 'Image lib   | Imgs/sec'

    @property
    def data_dir(self) -> str:
        return self._data_dir

    @data_dir.setter
    def data_dir(self, data_dir: str):
        self._data_dir = data_dir
        if self._num_items is not None:
            self.item_list = get_img_filenames(data_dir, self.num_items)

    @property
    def num_items(self) -> int:
        return self._num_items

    @num_items.setter
    def num_items(self, num_items: int):
        self.item_list = get_img_filenames(self.data_dir, num_items)
        self._num_items = num_items

    @property
    def results(self) -> dict:
        results = super().results
        return {func_name: (1 / results[func_name]) * len(self.item_list) for func_name in results}
