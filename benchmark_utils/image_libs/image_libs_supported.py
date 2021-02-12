from dataclasses import dataclass


@dataclass
class ImageLibCfg:
    lib_name: str
    package: str
    # import_name: str
    installation_type: str = 'pip'


image_libs_supported = {"torchvision": ImageLibCfg('torchvision', 'torchvision'),
                        "PIL": ImageLibCfg('PIL', 'pillow'),
                        "cv2": ImageLibCfg('cv2', 'opencv-python-headless'),
                        "jpeg4py": ImageLibCfg('jpeg4py', 'jpeg4py'),
                        "accimage": ImageLibCfg('accimage', 'accimage', installation_type='conda'),
                        "pyvips": ImageLibCfg('pyvips', 'pyvips', installation_type='pip'),
                        "skimage": ImageLibCfg('skimage', 'scikit-image'),
                        "imageio": ImageLibCfg('imageio', 'imageio')}
