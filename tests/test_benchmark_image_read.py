from benchmark_utils.benchmark_image_read import BenchmarkImageRead


def test_benchmark_image_read():
    data_dir = 'tests/test_imgs'
    bench = BenchmarkImageRead(data_dir=data_dir)
    assert len(bench.item_list) == 2
    bench.data_dir = data_dir
    results = bench.results
    assert type(results) == dict
    assert results == {}
    bench()
    # assert results != {}

    # test_name_lib = ImageLibCfg(test_name, test_name)
    # image_libs_supported[test_name] = test_name_lib
    # image_read_dict[test_name] = {'read_func': lambda _: '', 'version': ''}
    test_func_dict = {'test_func': lambda _: '', 'version': ''}
    bench = BenchmarkImageRead(test_func_dict, data_dir)
    bench.run(num_repeats=1)


def test_benchmark_image_read_lib(img_lib):
    data_dir = 'tests/test_imgs'
    bench = BenchmarkImageRead(data_dir=data_dir)
    assert len(bench.item_list) == 2
    bench.data_dir = data_dir
    results = bench.results
    assert type(results) == dict
    assert results == {}
    bench()
    # assert results != {}

    # test_name_lib = ImageLibCfg(test_name, test_name)
    # image_libs_supported[test_name] = test_name_lib
    # image_read_dict[test_name] = {'read_func': lambda _: '', 'version': ''}
    test_func_dict = {'test_func': lambda _: '', 'version': ''}
    bench = BenchmarkImageRead(test_func_dict, data_dir)
    bench.run(num_repeats=1)
