# import pytest

from benchmark_utils.image_libs.image_libs import ImageLib, ImageLibs, ImageLibCfg, image_lib_available


def test_image_lib():
    test_name = 'test_name'
    image_lib_cfg = ImageLibCfg(lib_name=test_name, package=test_name)
    assert image_lib_cfg.lib_name == test_name
    image_lib = ImageLib(image_lib_cfg, read_func=lambda _: '')
    assert test_name in repr(image_lib)
    assert test_name in str(image_lib)
    # with pytest.raises(NotImplementedError):
    #     image_lib.read('')
    # with pytest.raises(TypeError, match="NoneType"):
    assert image_lib.read('__') == ''


def test_image_libs(img_lib):
    assert img_lib in image_lib_available
    # assert image_libs_dict.get(img_lib) is not None
    image_libs = ImageLibs()
    assert img_lib in image_libs.available
    assert 'Image Libs' in repr(image_libs)
    assert img_lib in repr(img_lib)
    assert img_lib in str(img_lib)
    img_lib_obj = image_libs[img_lib]
    img_lib_obj.read('tests/test_imgs/test_img_1.JPEG')
    image_libs[img_lib].read('tests/test_imgs/test_img_2.JPEG')


# def test_read_image():
#     if read_PIL is None:
#         pass
#     else:
#         read_PIL('tests/test_imgs/test_img_1.JPEG')
