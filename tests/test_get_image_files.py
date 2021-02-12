from benchmark_utils.image_libs.get_image_files import get_img_filenames


def test_get_image_filenames():
    test_data_dir = 'tests/test_imgs'
    filenames = get_img_filenames(test_data_dir)
    assert type(filenames) == list
    assert len(filenames) == 2

    filenames = get_img_filenames(test_data_dir, num_samples=1)
    assert len(filenames) == 1

    filenames = get_img_filenames(test_data_dir, num_samples=0)
    assert len(filenames) == 2
