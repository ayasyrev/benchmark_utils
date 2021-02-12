from benchmark_utils.image_libs.image_libs import (
    ImageLib, ImageLibs, ImageLibCfg, image_lib_available, image_libs_supported)
from benchmark_utils.image_libs.read_image import image_read_dict


def test_image_lib():
    test_name = 'test_name'
    image_lib_cfg = ImageLibCfg(lib_name=test_name, package=test_name)
    assert image_lib_cfg.lib_name == test_name
    image_lib_obj = ImageLib(image_lib_cfg, read_func=lambda _: '')
    assert test_name in repr(image_lib_obj)
    assert test_name in str(image_lib_obj)
    # with pytest.raises(NotImplementedError):
    #     image_lib.read('')
    # with pytest.raises(TypeError, match="NoneType"):
    assert image_lib_obj.read('__') == ''

    image_lib_available.append(test_name)
    test_name_lib = ImageLibCfg(test_name, test_name)
    image_libs_supported[test_name] = test_name_lib
    image_read_dict[test_name] = {'read_func': lambda _: '', 'version': ''}
    image_lib_obj = ImageLib(test_name_lib)
    assert test_name == image_lib_obj.lib_name
    assert test_name in repr(image_lib_obj)
    assert image_lib_obj.read('__') == ''


def test_image_libs(img_lib):
    assert img_lib in image_lib_available
    # assert image_libs_dict.get(img_lib) is not None
    image_libs_obj = ImageLibs()
    assert img_lib in image_libs_obj.available
    assert 'Image Libs' in repr(image_libs_obj)
    assert img_lib in repr(image_libs_obj)
    assert img_lib in str(image_libs_obj)
    img_lib_obj = image_libs_obj[img_lib]
    img_lib_obj.read('tests/test_imgs/test_img_1.JPEG')
    image_libs_obj[img_lib].read('tests/test_imgs/test_img_2.JPEG')

    test_name = 'test_name'
    image_lib_available.append(test_name)
    test_name_lib = ImageLibCfg(test_name, test_name)
    image_libs_supported[test_name] = test_name_lib
    image_read_dict[test_name] = {'read_func': lambda _: '', 'version': ''}
    image_libs_obj = ImageLibs()

    assert image_libs_obj[test_name] == test_name_lib
    assert test_name in image_libs_obj._libs
    assert test_name_lib == image_libs_obj._libs[test_name]
    assert test_name_lib in repr(image_libs_obj)
