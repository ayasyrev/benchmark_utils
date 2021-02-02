from benchmark_utils import benchmark
from time import sleep


def func_to_test():
    sleep(0.01)


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
    assert result < (sleep_time * 1.05)
    assert result > (sleep_time / 1.05)
    assert str(bench) == name_func
    bench(1)
    bench.run()
    bench.run(name_func)
    bench.run('')
    bench = benchmark.Benchmark(func_to_test)
    assert repr(bench) == 'func_to_test'
    benchmark.benchmark(func_to_test)
