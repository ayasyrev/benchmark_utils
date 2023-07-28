# Benchmark utils

Utils for benchmark - wrapper over python timeit.

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/benchmark-utils)](https://pypi.org/project/benchmark-utils/)
[![PyPI Status](https://badge.fury.io/py/benchmark-utils.svg)](https://badge.fury.io/py/benchmark-utils)  
[![Tests](https://github.com/ayasyrev/benchmark_utils/workflows/Tests/badge.svg)](https://github.com/ayasyrev/benchmark_utils/actions?workflow=Tests)  [![Codecov](https://codecov.io/gh/ayasyrev/benchmark_utils/branch/main/graph/badge.svg)](https://codecov.io/gh/ayasyrev/benchmark_utils)  

Tested on python 3.7 - 3.11

## Install

Install from pypi:  

`pip install benchmark_utils`

Or install from github repo:

`pip install git+https://github.com/ayasyrev/benchmark_utils.git`

## Basic use.

Lets benchmark some (dump) functions.


```python
from time import sleep

def func_to_test_1(sleep_time: float = 0.1, mult: int = 1) -> None:
    """simple 'sleep' func for test"""
    sleep(sleep_time * mult)


def func_to_test_2(sleep_time: float = 0.11, mult: int = 1) -> None:
    """simple 'sleep' func for test"""
    sleep(sleep_time * mult)

```

Let's create benchmark.


```python
from benchmark_utils import Benchmark
```


```python
bench = Benchmark(
    [func_to_test_1, func_to_test_2],
)
```


```python
bench
```
<details open> <summary>output</summary>  
    <pre>Benchmark(func_to_test_1, func_to_test_2)</pre>
</details>



Now we can benchmark that functions.


```python
bench()
```
<details open> <summary>output</summary>  
    <pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"> Func name  | Sec <span style="color: #800080; text-decoration-color: #800080">/</span> run
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">func_to_test_1:   <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.10</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.0</span>%
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">func_to_test_2:   <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.11</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">-9.6</span>%
</pre>

</details>


We can run it again, all functions, some of it, exclude some and change number of repeats.


```python
bench.run(num_repeats=10)
```
<details open> <summary>output</summary>  
    <pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"> Func name  | Sec <span style="color: #800080; text-decoration-color: #800080">/</span> run
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">func_to_test_1:   <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.10</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.0</span>%
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">func_to_test_2:   <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.11</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">-8.8</span>%
</pre>

</details>


After run, we can prunt results - sorted or not, reversed, compare results with best or not. 


```python
bench.print_results(reverse=True)
```
<details open> <summary>output</summary>  
    <pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"> Func name  | Sec <span style="color: #800080; text-decoration-color: #800080">/</span> run
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">func_to_test_2:   <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.11</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.0</span>%
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">func_to_test_1:   <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.10</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">9.7</span>%
</pre>

</details>


We can add functions to bencmark as list of funtions (or partial) ar as dictionary: `{"name": function}`.


```python
bench = Benchmark([
    func_to_test_1,
    partial(func_to_test_1, 0.12),
    partial(func_to_test_1, sleep_time=0.11),
])

```


```python
bench
```
<details open> <summary>output</summary>  
    <pre>Benchmark(func_to_test_1, func_to_test_1(0.12), func_to_test_1(sleep_time=0.11))</pre>
</details>




```python
bench.run()
```
<details open> <summary>output</summary>  
    <pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"> Func name  | Sec <span style="color: #800080; text-decoration-color: #800080">/</span> run
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">func_to_test_1:   <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.10</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.0</span>%
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">func_to_test_1</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">sleep_time</span>=<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.11</span><span style="font-weight: bold">)</span>:   <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.11</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">-8.9</span>%
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">func_to_test_1</span><span style="font-weight: bold">(</span><span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.12</span><span style="font-weight: bold">)</span>:   <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.12</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">-16.5</span>%
</pre>

</details>



```python
bench = Benchmark({
    "func_1": func_to_test_1,
    "func_2": func_to_test_2,
})
```


```python
bench
```
<details open> <summary>output</summary>  
    <pre>Benchmark(func_1, func_2)</pre>
</details>


