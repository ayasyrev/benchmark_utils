""" tests for benchmarks
"""
# pylint: disable=protected-access

from functools import partial
from time import sleep

from pytest import CaptureFixture

from benchmark_utils import benchmark
from benchmark_utils.benchmark import get_func_name


def func_to_test_1(sleep_time: float = 0.1, mult: int = 1) -> None:
    """simple 'sleep' func for test"""
    sleep(sleep_time * mult)


def func_to_test_2(sleep_time: float = 0.1, mult: int = 1) -> None:
    """simple 'sleep' func for test"""
    sleep(sleep_time * mult)


def test_func_name():
    """test for get_func_name as arg"""
    func_name = get_func_name(func_to_test_1)
    assert func_name == "func_to_test_1"
    func_name = get_func_name(func=partial(func_to_test_1, sleep_time=0.2))
    assert func_name == "func_to_test_1(sleep_time=0.2)"
    func_name = get_func_name(func=partial(func_to_test_1, 0.2))
    assert func_name == "func_to_test_1(0.2)"
    func_name = get_func_name(func=partial(func_to_test_1, 0.2, 2))
    assert func_name == "func_to_test_1(0.2, 2)"
    func_name = get_func_name(func=partial(func_to_test_1, 0.2, mult=2))
    assert func_name == "func_to_test_1(0.2, mult=2)"


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
    """test for equal func"""
    assert equal_near(1.0, 1.0099)
    assert equal_near(1.0, 0.999)
    assert not equal_near(1.0, 1.112)
    assert not equal_near(1.0, 0.9)


def test_benchmark():
    """base tests for bench"""
    name_func = "test_func_1"
    sleep_time = 0.01
    # func as dict
    bench = benchmark.Benchmark({name_func: lambda: sleep(sleep_time)})
    assert bench.num_repeats == 5
    assert bench.results == {}
    assert name_func in repr(bench)

    # ran as __call__
    bench()
    result = bench.results[name_func]
    assert equal_near(result, sleep_time, threshold=0.5)
    assert name_func in str(bench)
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
    bench = benchmark.Benchmark(func_to_test_1)
    assert "func_to_test_1" in repr(bench)
    bench = benchmark.Benchmark([func_to_test_1, func_to_test_2])
    assert "func_to_test_1" in repr(bench)
    assert "func_to_test_2" in repr(bench)
    bench()
    assert bench._results is not None
    assert len(bench._results) == 2

    # run only one func
    bench.run(func_name="func_to_test_1")
    assert bench._results is not None
    assert len(bench._results) == 1
    assert len(bench.func_dict) == 2
    assert "func_to_test_1" in bench._results
    # exclude one
    bench.run(exclude="func_to_test_1")
    assert bench._results is not None
    assert len(bench._results) == 1
    assert "func_to_test_1" not in bench._results
    # exclude one as list of func
    bench.run(exclude=["func_to_test_2"])
    assert bench._results is not None
    assert len(bench._results) == 1
    assert "func_to_test_2" not in bench._results
    # run only one func, as list of funcs
    bench.run(func_name=["func_to_test_1"])
    assert bench._results is not None
    assert len(bench._results) == 1
    assert len(bench.func_dict) == 2
    assert "func_to_test_1" in bench._results
    # wrong name, nothing to test, empty _results
    bench.run(func_name="func_to_test_wrong_1")
    assert not bench._results
    assert len(bench._results) == 0
    # wrong name in list, only one test
    bench.run(func_name=["func_to_test_wrong_2", "func_to_test_2"])
    assert len(bench._results) == 1
    assert "func_to_test_2" in bench._results
    # wrong name in exclude -> all tests
    bench.run(exclude=["func_to_test_wrong_3"])
    assert bench._results is not None
    assert len(bench._results) == 2


def test_benchmark_print(capsys: CaptureFixture[str]):
    """test printing from benchmark"""
    bench = benchmark.Benchmark(
        [
            func_to_test_1,
            partial(func_to_test_2, 0.12),
            partial(func_to_test_1, sleep_time=0.11),
        ]
    )
    bench()
    captured = capsys.readouterr()
    assert "func_to_test_2(0.12)" in captured.out
    assert "func_to_test_1:" in captured.out
    bench.print_results()
    captured = capsys.readouterr()
    out = captured.out
    assert "func_to_test_2(0.12)" in out
    assert "func_to_test_1:" in out
    out_splitted = out.split("\n")
    assert len(out_splitted) == 5
    assert out_splitted[1].startswith("func_to_test_1")
    assert out_splitted[2].startswith("func_to_test_1(sleep_time=0.11)")
    assert out_splitted[3].startswith("func_to_test_2(0.12)")

    # not sorted
    bench.print_results(sort=False)
    out_splitted = capsys.readouterr().out.split("\n")
    assert len(out_splitted) == 5
    assert out_splitted[1].startswith("func_to_test_1")
    assert out_splitted[2].startswith("func_to_test_2(0.12)")
    assert out_splitted[3].startswith("func_to_test_1(sleep_time=0.11)")

    # reversed
    bench.print_results(reverse=True)
    out_splitted = capsys.readouterr().out.split("\n")
    assert out_splitted[1].startswith("func_to_test_2(0.12)")
    assert out_splitted[2].startswith("func_to_test_1(sleep_time=0.11)")
    assert out_splitted[3].startswith("func_to_test_1")

    # no compare
    bench.print_results(compare=False)
    out = capsys.readouterr().out
    assert "%" not in out


def test_benchmark_iter(capsys: CaptureFixture[str]):
    """base tests for bench iter"""
    name_func = "test_func"
    len_item_list = 3
    sleep_time = 0.01
    list_item_sleep_time = len_item_list * [sleep_time]
    bench = benchmark.BenchmarkIter(
        func={name_func: func_to_test_1},
        item_list=list_item_sleep_time,
    )
    assert name_func in repr(bench)
    bench()

    # check print. !check result.
    captured = capsys.readouterr()
    assert name_func in captured.out
    result = bench.results[name_func]
    assert equal_near(result, sleep_time * len_item_list, threshold=0.5)
    # check print
    bench.print_results_per_item()
    captured = capsys.readouterr()
    assert name_func in captured.out

    # w/ exceptions
    bench = benchmark.BenchmarkIter(
        func={name_func: func_to_test_1},
        item_list=[0.01, -1],
    )
    bench()
    assert len(bench.exceptions) == 1
    captured = capsys.readouterr()
    assert "exceptions" in captured.out


def func_with_exception(in_value: bool) -> None:
    """dummy func, return exception."""
    if in_value:
        pass
    else:
        raise ValueError("error")


def func_dummy(in_value: bool) -> None:  # pylint: disable=unused-argument
    """dummy empty function."""


def test_benchmark_iter_wrong_item():
    """test bench w/ and w/o wrong item in item list"""
    item_list = [True, False]
    bench = benchmark.BenchmarkIter(
        func=func_with_exception,
        item_list=item_list,
    )
    assert len(bench.exceptions) == 0
    assert "func_with_exception" in repr(bench)
    bench()
    assert len(bench.exceptions) == 1

    # dict of func
    # run w/o exceptions
    bench = benchmark.BenchmarkIter(
        func={
            "func_1": func_with_exception,
            "func_2": func_dummy,
        },
        item_list=[True, True],
    )
    assert "func_1" in repr(bench)
    assert "func_2" in repr(bench)
    bench()
    assert len(bench.exceptions) == 0

    # run w/ exception
    bench = benchmark.BenchmarkIter(
        func={
            "func_1": func_with_exception,
            "func_2": func_dummy,
        },
        item_list=item_list,
    )
    bench()
    assert len(bench.exceptions) == 1
    assert len(bench._results) == 2

    # # new run w/o exceptions
    bench.run("func_2")
    assert bench._results is not None
    assert len(bench.exceptions) == 0
    assert len(bench._results) == 1
