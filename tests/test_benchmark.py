from benchmark_utils import benchmark
from time import sleep


def test_benchmark():
    name_func = 'test_func'
    sleep_time = 0.01
    bench = benchmark.Benchmark({name_func: lambda: sleep(sleep_time)})
    bench()
    result = bench.results[name_func]
    assert result < (sleep_time * 1.05)
    assert result > (sleep_time / 1.05)
    assert str(bench) == name_func
