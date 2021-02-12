from pathlib import Path
from typing import List


IMG_EXT = [".JPEG", '.JPG', '.jpeg', '.jpg']


def get_img_filenames(data_dir: str, num_samples: int = 200) -> List[str]:
    """Return list of num_samples image filenames from data_dir.
    If num_samples == 0 return list of ALL images.

    Args:
        data_dir (str):
        num_samples (int, optional): Number of samples to return. Defaults to 200.
        If num_samples == 0 return list of ALL images.


    Returns:
        List[str]: List of filnames
    """
    image_filenames = [str(fn) for fn in Path(data_dir).rglob("*.*") if fn.suffix in IMG_EXT]
    if num_samples != 0:
        image_filenames = image_filenames[:num_samples]
    return image_filenames
