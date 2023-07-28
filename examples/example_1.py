"""Simple benchmark example."""
from time import sleep

from benchmark_utils import Benchmark


def func_to_test_1(sleep_time: float = 0.1, mult: int = 1) -> None:
    """simple 'sleep' func for test"""
    sleep(sleep_time * mult)


def func_to_test_2(sleep_time: float = 0.11, mult: int = 1) -> None:
    """simple 'sleep' func for test"""
    sleep(sleep_time * mult)


bench = Benchmark(
    [func_to_test_1, func_to_test_2],
)


if __name__ == "__main__":
    bench()
