import pytest

from benchmark_utils.image_libs import ImageLib, ImageLibs


def test_image_lib():
    image_lib = ImageLib()
    assert 'ImageLib' in repr(image_lib)
    assert 'ImageLib' in str(image_lib)
    with pytest.raises(NotImplementedError):
        image_lib.read('')


def test_image_libs(img_lib):
    image_libs = ImageLibs()
    assert img_lib in image_libs.available
    assert 'Image Libs' in repr(image_libs)
    assert img_lib in repr(img_lib)
    assert img_lib in str(img_lib)
    img_lib_obj = image_libs[img_lib]
    img_lib_obj.read('tests/test_imgs/test_img_1.JPEG')
    image_libs[img_lib].read('tests/test_imgs/test_img_2.JPEG')
