<!-- cell -->
---
hide:
  - navigation
---
<!-- cell -->
# Benchmark utils
<!-- cell -->
Utils for benchmark - wrapper over python timeit.
<!-- cell -->
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/benchmark-utils)](https://pypi.org/project/benchmark-utils/)
[![PyPI Status](https://badge.fury.io/py/benchmark-utils.svg)](https://badge.fury.io/py/benchmark-utils)  
[![Tests](https://github.com/ayasyrev/benchmark_utils/workflows/Tests/badge.svg)](https://github.com/ayasyrev/benchmark_utils/actions?workflow=Tests)  [![Codecov](https://codecov.io/gh/ayasyrev/benchmark_utils/branch/main/graph/badge.svg)](https://codecov.io/gh/ayasyrev/benchmark_utils)
<!-- cell -->
Tested on python 3.8 - 3.12
<!-- cell -->
## Install
<!-- cell -->
Install from pypi:  

`pip install benchmark_utils`

Or install from github repo:

`pip install git+https://github.com/ayasyrev/benchmark_utils.git`
<!-- cell -->
## Basic use.
<!-- cell -->
Lets benchmark some (dummy) functions.
<!-- cell -->
<details open> <summary>output</summary>  
```python
from time import sleep


def func_to_test_1(sleep_time: float = 0.1, mult: int = 1) -> None:
    """simple 'sleep' func for test"""
    sleep(sleep_time * mult)


def func_to_test_2(sleep_time: float = 0.11, mult: int = 1) -> None:
    """simple 'sleep' func for test"""
    sleep(sleep_time * mult)</details>

<!-- cell -->
<details open> <summary>output</summary>  

Let's create benchmark.</details>

<!-- cell -->
<details open> <summary>output</summary>  
```python
from benchmark_utils import Benchmark
```</details>

<!-- cell -->
<details open> <summary>output</summary>  
```python
bench = Benchmark(
    [func_to_test_1, func_to_test_2],
)
```</details>

<!-- cell -->
```python
bench
```
<details open> <summary>output</summary>  




    Benchmark(func_to_test_1, func_to_test_2)</details>

<!-- cell -->
Now we can benchmark that functions.
<!-- cell -->
```python
# we can run bench.run() or just:
bench()
```
<details open> <summary>output</summary>  


<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"></pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"> Func name  | Sec <span style="color: #800080; text-decoration-color: #800080">/</span> run
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">func_to_test_1:   <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.10</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.0</span>%
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">func_to_test_2:   <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.11</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">-9.1</span>%
</pre></details>

<!-- cell -->
We can run it again, all functions, some of it, exclude some and change number of repeats.
<!-- cell -->
```python
bench.run(num_repeats=10)
```
<details open> <summary>output</summary>  


<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"></pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"> Func name  | Sec <span style="color: #800080; text-decoration-color: #800080">/</span> run
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">func_to_test_1:   <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.10</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.0</span>%
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">func_to_test_2:   <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.11</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">-9.1</span>%
</pre></details>

<!-- cell -->
After run, we can print results - sorted or not, reversed, compare results with best or not.
<!-- cell -->
```python
bench.print_results(reverse=True)
```
<details open> <summary>output</summary>  


<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"> Func name  | Sec <span style="color: #800080; text-decoration-color: #800080">/</span> run
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">func_to_test_2:   <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.11</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.0</span>%
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">func_to_test_1:   <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.10</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">10.0</span>%
</pre></details>

<!-- cell -->
We can add functions to benchmark as list of functions (or partial) or as dictionary: `{"name": function}`.
<!-- cell -->
<details open> <summary>output</summary>  
```python
bench = Benchmark(
    [
        func_to_test_1,
        partial(func_to_test_1, 0.12),
        partial(func_to_test_1, sleep_time=0.11),
    ]
)
```</details>

<!-- cell -->
```python
bench
```
<details open> <summary>output</summary>  




    Benchmark(func_to_test_1, func_to_test_1(0.12), func_to_test_1(sleep_time=0.11))</details>

<!-- cell -->
```python
bench.run()
```
<details open> <summary>output</summary>  


<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"></pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"> Func name  | Sec <span style="color: #800080; text-decoration-color: #800080">/</span> run
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">func_to_test_1:   <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.10</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.0</span>%
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">func_to_test_1</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">sleep_time</span>=<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.11</span><span style="font-weight: bold">)</span>:   <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.11</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">-9.1</span>%
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">func_to_test_1</span><span style="font-weight: bold">(</span><span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.12</span><span style="font-weight: bold">)</span>:   <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.12</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">-16.7</span>%
</pre></details>

<!-- cell -->
<details open> <summary>output</summary>  
```python
bench = Benchmark(
    {
        "func_1": func_to_test_1,
        "func_2": func_to_test_2,
    }
)
```</details>

<!-- cell -->
```python
bench
```
<details open> <summary>output</summary>  




    Benchmark(func_1, func_2)</details>

<!-- cell -->
When we run benchmark script in terminal, we got pretty progress thanks to rich. Lets run example_1.py from example folder:
<!-- cell -->
![example_1](images/run_example_1.gif)
<!-- cell -->
## BenchmarkIter
<!-- cell -->
With BenchmarkIter we can benchmark functions over iterables, for example read list of files or run functions with different arguments.
<!-- cell -->
<details open> <summary>output</summary>  
```python
def func_to_test_1(x: int) -> None:
    """simple 'sleep' func for test"""
    sleep(0.01)


def func_to_test_2(x: int) -> None:
    """simple 'sleep' func for test"""
    sleep(0.015)


dummy_params = list(range(10))
```</details>

<!-- cell -->
<details open> <summary>output</summary>  
```python
from benchmark_utils import BenchmarkIter

bench = BenchmarkIter(
    func=[func_to_test_1, func_to_test_2],
    item_list=dummy_params,
)
```</details>

<!-- cell -->
```python
bench()
```
<details open> <summary>output</summary>  


<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"></pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"> Func name  | Items/sec
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">func_to_test_1:  <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">97.93</span>
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">func_to_test_2:  <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">65.25</span>
</pre></details>

<!-- cell -->
We can run it again, all functions, some of it, exclude some and change number of repeats.
And we can limit number of items with `num_samples` argument:
`bench.run(num_samples=5)`
<!-- cell -->
## Multiprocessing
<!-- cell -->
By default we tun functions in one thread.  
But we can use multiprocessing with `multiprocessing=True` argument:
`bench.run(multiprocessing=True)`
It will use all available cpu cores.
And we can use `num_workers` argument to limit used cpu cores:
`bench.run(multiprocessing=True, num_workers=2)`
<!-- cell -->
```python
bench.run(multiprocessing=True, num_workers=2)
```
<details open> <summary>output</summary>  


<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"></pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"> Func name  | Items/sec
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">func_to_test_1: <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">173.20</span>
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">func_to_test_2: <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">120.80</span>
</pre></details>
