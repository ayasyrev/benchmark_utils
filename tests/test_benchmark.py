from benchmark_utils import benchmark
from time import sleep


def func_to_test(sleep_time: float = 0.1) -> None:
    sleep(sleep_time)

def func_to_test_2(sleep_time: float = 0.1) -> None:
    sleep(sleep_time)


def equal_near(item_1: float, item_2: float, thresold: float = 0.1) -> bool:
    """Is two item close to equl?
    Return True is difference less than thresold.

    Args:
        item_1 (float): First item.
        item_2 (float): Second item.
        thresold (float, optional): Thresold for compare. Defaults to 0.01.

    Returns:
        bool: Return True if difference less than thresold.
    """
    return abs(1 - (item_1 / item_2)) < thresold


def test_equal_near():
    assert equal_near(1., 1.0099)
    assert equal_near(1., 0.999)
    assert not equal_near(1., 1.112)
    assert not equal_near(1., 0.9)


def test_benchmark():
    name_func = 'test_func'
    sleep_time = 0.01
    bench = benchmark.Benchmark({name_func: lambda: sleep(sleep_time)})
    assert bench.num_repeats == 5
    assert bench.results == {}
    assert bench.__repr__() == name_func
    assert repr(bench) == name_func
    bench()
    result = bench.results[name_func]
    assert equal_near(result, sleep_time, thresold=0.5)
    assert str(bench) == name_func
    bench(1)
    bench.run()
    bench.run(name_func)
    bench.run('')
    bench = benchmark.Benchmark(func_to_test)
    assert repr(bench) == 'func_to_test'
    benchmark.benchmark(func_to_test)
    bench = benchmark.Benchmark([func_to_test, func_to_test_2])
    assert repr(bench) == 'func_to_test, func_to_test_2'
    bench()
    bench.print_results()
    bench.print_results(sort=True)
    bench.print_results(results={'test_func': 0.1}, results_header='test_func  | sec')
    bench.print_results(results={'test_func': 0.1}, results_header='test_func  | sec', compare=True)


def test_benchmark_iter():
    name_func = 'test_func'
    len_item_list = 3
    sleep_time = 0.01
    list_iten_sleep_time = len_item_list * [sleep_time]
    bench = benchmark.BenchmarkIter(func={name_func: func_to_test}, item_list=list_iten_sleep_time)
    assert bench.__repr__() == name_func
    assert repr(bench) == name_func
    bench()
    result = bench.results[name_func]
    print(result)
    assert equal_near(result, sleep_time * len_item_list, thresold=0.5)
    bench.print_results_per_item()


def func_with_exception(input: bool) -> None:
    if input:
        pass
    else:
        raise Exception('error')


def test_benchmark_iter_wrong_item():
    item_list = [True, False]
    bench = benchmark.BenchmarkIter(func=func_with_exception, item_list=item_list)
    assert bench.exeptions is None
    assert bench.__repr__() == 'func_with_exception'
    assert repr(bench) == 'func_with_exception'
    bench()
    assert bench.exeptions is not None
