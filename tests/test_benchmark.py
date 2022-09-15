from benchmark_utils import benchmark
from time import sleep


def func_to_test(sleep_time: float = 0.1) -> None:
    sleep(sleep_time)


def func_to_test_2(sleep_time: float = 0.1) -> None:
    sleep(sleep_time)


def equal_near(item_1: float, item_2: float, threshold: float = 0.1) -> bool:
    """Is two item close to equal?
    Return True is difference less than threshold.

    Args:
        item_1 (float): First item.
        item_2 (float): Second item.
        threshold (float, optional): Threshold for compare. Defaults to 0.01.

    Returns:
        bool: Return True if difference less than threshold.
    """
    return abs(1 - (item_1 / item_2)) < threshold


def test_equal_near():
    assert equal_near(1.0, 1.0099)
    assert equal_near(1.0, 0.999)
    assert not equal_near(1.0, 1.112)
    assert not equal_near(1.0, 0.9)


def test_benchmark():
    name_func = "test_func"
    sleep_time = 0.01
    # func as dict
    bench = benchmark.Benchmark({name_func: lambda: sleep(sleep_time)})
    assert bench.num_repeats == 5
    assert bench.results == {}
    assert bench.__repr__() == name_func
    assert repr(bench) == name_func
    # ran as __call__
    bench()
    result = bench.results[name_func]
    assert equal_near(result, sleep_time, threshold=0.5)
    assert str(bench) == name_func
    assert bench._results is not None
    assert len(bench._results) == 1
    assert len(bench._results[name_func]) == 5
    # run 1 repeat
    bench(1)
    assert bench._results is not None
    assert len(bench._results) == 1
    assert len(bench._results[name_func]) == 1
    # ran at .run
    bench.run()
    bench.run(name_func)
    bench.run("")
    # bench one func
    bench = benchmark.Benchmark(func_to_test)
    assert repr(bench) == "func_to_test"
    bench = benchmark.Benchmark([func_to_test, func_to_test_2])
    assert repr(bench) == "func_to_test, func_to_test_2"
    bench()
    assert bench._results is not None
    assert len(bench._results) == 2
    # run prints
    # todo test print results
    bench.print_results()
    bench.print_results(sort=True)
    bench.print_results(results={"test_func": 0.1}, results_header="test_func  | sec")
    bench.print_results(
        results={"test_func": 0.1}, results_header="test_func  | sec", compare=True
    )
    assert len(bench.func_dict) == 2
    # run only one func
    bench.run(func_name="func_to_test")
    assert bench._results is not None
    assert len(bench._results) == 1
    assert len(bench.func_dict) == 2
    assert "func_to_test" in bench._results
    # exclude one
    bench.run(exclude="func_to_test")
    assert bench._results is not None
    assert len(bench._results) == 1
    assert "func_to_test" not in bench._results
    # exclude one as list of func
    bench.run(exclude=["func_to_test_2"])
    assert bench._results is not None
    assert len(bench._results) == 1
    assert "func_to_test_2" not in bench._results
    # run only one func, as list of funcs
    bench.run(func_name=["func_to_test"])
    assert bench._results is not None
    assert len(bench._results) == 1
    assert len(bench.func_dict) == 2
    assert "func_to_test" in bench._results
    # wrong name, nothing to test, empty _results
    bench.run(func_name="func_to_test_wrong_1")
    assert bench._results == {}
    assert len(bench._results) == 0
    # wrong name in list, only one test
    bench.run(func_name=["func_to_test_wrong_2", "func_to_test_2"])
    assert len(bench._results) == 1
    assert "func_to_test_2" in bench._results
    # wrong name in exclude -> all tests
    bench.run(exclude=["func_to_test_wrong_3"])
    assert bench._results is not None
    assert len(bench._results) == 2
    # assert "func_to_test_2" not in bench._results


def test_benchmark_iter():
    name_func = "test_func"
    len_item_list = 3
    sleep_time = 0.01
    list_item_sleep_time = len_item_list * [sleep_time]
    bench = benchmark.BenchmarkIter(
        func={name_func: func_to_test}, item_list=list_item_sleep_time
    )
    assert bench.__repr__() == name_func
    assert repr(bench) == name_func
    bench()
    result = bench.results[name_func]
    print(result)
    assert equal_near(result, sleep_time * len_item_list, threshold=0.5)
    bench.print_results_per_item()


def func_with_exception(input: bool) -> None:
    if input:
        pass
    else:
        raise Exception("error")


def func_dummy(input: bool) -> None:
    pass


def test_benchmark_iter_wrong_item():
    item_list = [True, False]
    bench = benchmark.BenchmarkIter(func=func_with_exception, item_list=item_list)
    assert bench.exceptions is None
    assert bench.__repr__() == "func_with_exception"
    assert repr(bench) == "func_with_exception"
    bench()
    assert bench.exceptions is not None
    assert len(bench.exceptions) == 1
    # dict of func
    bench = benchmark.BenchmarkIter(
        func={
            "func_1": func_with_exception,
            "func_2": func_dummy,
        },
        item_list=item_list,
    )
    assert bench.exceptions is None
    assert bench.__repr__() == "func_1, func_2"
    assert repr(bench) == "func_1, func_2"
    # run
    bench()
    assert bench._results is not None
    assert bench.exceptions is not None
    assert len(bench.exceptions) == 1
    assert len(bench._results) == 2
    # new run w/0 exceptions
    bench.run("func_2")
    assert bench._results is not None
    assert bench.exceptions is None
    assert len(bench._results) == 1
