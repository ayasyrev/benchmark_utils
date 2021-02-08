from benchmark_utils.image_libs import ImageLibs


def test_image_libs(img_lib):
    image_libs = ImageLibs()
    assert img_lib in image_libs.available
    assert 'Image Libs' in repr(image_libs)
    assert img_lib in repr(img_lib)
