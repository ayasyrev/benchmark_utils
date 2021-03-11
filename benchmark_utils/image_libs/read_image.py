# pyright: reportMissingImports=false
# pyright: reportMissingModuleSource=false
import importlib

# import numpy as np
# from importlib.metadata import version
import pkg_resources

PIL_AVAILABLE = importlib.util.find_spec("PIL") is not None

if PIL_AVAILABLE:
    from PIL import Image, __version__
    PIL_version = __version__
    # self.image_open = Image.open

    def read_PIL(file_name: str) -> object:
        with open(file_name, 'rb') as file:
            img = Image.open(file)
            return img.convert('RGB')
else:
    read_PIL = None
    PIL_version = None


CV2_AVAILABLE = importlib.util.find_spec("cv2") is not None
if CV2_AVAILABLE:
    import cv2  # type:False

    def read_cv2(image_path: str) -> object:
        img = cv2.imread(image_path)
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2_version = cv2.__version__
else:
    read_cv2 = None
    cv2_version = None


IMAGEIO_AVAILABLE = importlib.util.find_spec("imageio") is not None
if IMAGEIO_AVAILABLE:
    import imageio

    def read_imageio(image_path: str) -> object:
        return imageio.imread(image_path)
    imageio_version = imageio.__version__
else:
    read_imageio = None
    imageio_version = None


PYVIPS_AVAILABLE = importlib.util.find_spec("pyvips") is not None
if PYVIPS_AVAILABLE:
    import numpy as np
    import pyvips

    def read_pyvips(image_path: str) -> np.array:
        image = pyvips.Image.new_from_file(image_path, access="sequential")

        memory_image = image.write_to_memory()
        numpy_image = np.ndarray(buffer=memory_image, dtype=np.uint8, shape=[image.height, image.width, image.bands])

        return numpy_image
    pyvips_version = pyvips.__version__
else:
    read_pyvips = None
    pyvips_version = None

SKIMAGE_AVAILABLE = importlib.util.find_spec("skimage") is not None
if SKIMAGE_AVAILABLE:
    import skimage
    import skimage.io as io

    def read_skimage(image_path: str) -> object:
        return io.imread(image_path, plugin="matplotlib")
    skimage_version = skimage.__version__
else:
    read_skimage = None
    skimage_version = None


JPEG4PY_AVAILABLE = importlib.util.find_spec("jpeg4py") is not None
if JPEG4PY_AVAILABLE:
    import jpeg4py

    def read_jpeg4py(image_path: str) -> object:
        return jpeg4py.JPEG(image_path).decode()
    jpeg4py_version = pkg_resources.get_distribution('jpeg4py').version
else:
    read_jpeg4py = None
    jpeg4py_version = None


TORCHVISION_AVAILABLE = importlib.util.find_spec("torchvision") is not None
if TORCHVISION_AVAILABLE:
    from torchvision import __version__ as TV_version
    TORCHVISION_AVAILABLE = int(TV_version.split('.')[1]) >= 8
    if TORCHVISION_AVAILABLE:
        from torchvision.io import read_image

        def read_torchvision(img_fn):
            img = read_image(img_fn)
            return img
    else:
        read_torchvision = None
        TV_version = None
else:
    read_torchvision = None
    TV_version = None


ACCIMAGE_AVAILABLE = importlib.util.find_spec("accimage") is not None
if ACCIMAGE_AVAILABLE:
    import accimage

    def read_accimage(image_path: str) -> accimage.Image:
        return accimage.Image(image_path)
    # accimage_version = version('accimage')
    accimage_version = pkg_resources.get_distribution('accimage').version
else:
    read_accimage = None
    accimage_version = None


image_read_dict = {
    'PIL': {'read_func': read_PIL, 'version': PIL_version},
    'cv2': {'read_func': read_cv2, 'version': cv2_version},
    'imageio': {'read_func': read_imageio, 'version': imageio_version},
    'jpeg4py': {'read_func': read_jpeg4py, 'version': jpeg4py_version},
    'skimage': {'read_func': read_skimage, 'version': skimage_version},
    'torchvision': {'read_func': read_torchvision, 'version': TV_version},
    'accimage': {'read_func': read_accimage, 'version': accimage_version},
    'pyvips': {'read_func': read_pyvips, 'version': pyvips_version},
}
