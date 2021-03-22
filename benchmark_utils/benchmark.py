from timeit import timeit
from typing import Union, Dict, List, Callable
from tqdm.autonotebook import tqdm


def benchmark(func: Callable, num_repeats: int = 5, name: str = '') -> List[float]:
    """Return list of run times for func, num_repeats times"""
    run_times = []
    with tqdm(total=num_repeats, leave=False) as pbar:
        for i in range(num_repeats):
            pbar.set_description(f"{name}: run {i + 1}/{num_repeats}")
            run_times.append(timeit(func, number=1))
            pbar.update(1)
    return run_times


class Benchmark:
    """Bench func, num_repeats times"""
    def __init__(self, func: Union[callable, Dict[str, callable]], num_repeats: int = 5):
        self.num_repeats = num_repeats
        self._results = None
        if type(func) == dict:
            self.bench_func_dict = func
        else:
            self.bench_func_dict = {func.__name__: func}
        self._benchmark = benchmark
        self.results_header = ' Func name  | Sec / run'

    def run(self, func_name: Union[str, None] = None, num_repeats: Union[int, None] = None) -> None:
        if func_name is None:
            self._run(self.bench_func_dict, num_repeats)
        else:
            func = self.bench_func_dict.get(func_name)
            if func is not None:  # todo - add List as input
                bench_func_dict = {func_name: func}
                self._run(bench_func_dict, num_repeats)
            else:
                print(f'Func_name {func_name} is not in bench_func_dict')

    def _run(self, bench_func_dict: dict, num_repeats: Union[int, None] = None) -> None:
        if num_repeats is None:
            num_repeats = self.num_repeats
        self._results = {}  # ? if exists add new
        progress_bar = tqdm(total=len(bench_func_dict.keys()))
        for func_name in bench_func_dict:
            progress_bar.set_description(f"running {func_name}")
            self._results[func_name] = self._run_benchmark(func_name, num_repeats=num_repeats)
            progress_bar.update(1)

        self.print_results()

    def _run_benchmark(self, func_name: str, num_repeats: int):
        return self._benchmark(self.bench_func_dict[func_name], num_repeats)

    def __call__(self, num_repeats: Union[int, None] = None) -> None:
        if num_repeats is None:
            num_repeats = self.num_repeats
        self._run(self.bench_func_dict, num_repeats)

    @property
    def results(self) -> dict:
        if self._results is None:
            return {}
        else:
            result = {}
            for res in self._results:
                result[res] = sum(self._results[res]) / len(self._results[res])
            return result

    def print_results(self, results=None, results_header=None, sort=True, reverse=False, compare=False) -> None:
        self._print_results(results=results, results_header=None, sort=sort, reverse=reverse, compare=compare)

    def _print_results(self, results=None, results_header=None, sort=True, reverse=False, compare=False) -> None:
        if results_header is None:
            results_header = self.results_header
        if results is None:
            results = self.results
        print(results_header)
        func_names = list(results.keys())
        if sort:
            func_names = sorted(results, key=results.get, reverse=reverse)
            results = {func_name: results[func_name] for func_name in func_names}
        best_res = results[func_names[0]]
        for func_name in func_names:
            line = f"{func_name:12}: {results[func_name]:6.2f}"
            if compare:
                line += f" {(best_res / results[func_name]) - 1:0.1%}"
            print(line)

    def __str__(self) -> str:
        return ', '.join(self.bench_func_dict.keys())

    def __repr__(self) -> str:
        return ', '.join(self.bench_func_dict.keys())


class BenchmarkIter(Benchmark):
    """Benchmark func over item_list"""
    def __init__(self, func: Union[callable, Dict[str, callable]], item_list: List = [], num_repeats: int = 5):
        super().__init__(func, num_repeats=num_repeats)
        self.item_list = item_list
        self.exeptions = None

    def _run_benchmark(self, func_name: str, num_repeats: int):
        return self._benchmark(self.run_func_iter(func_name), num_repeats, func_name)

    def run_func_iter(self, func_name: str) -> Callable:
        """Return func, that run func over item_list"""
        def inner(self=self, func_name=func_name):
            func = self.bench_func_dict[func_name]
            with tqdm(total=len(self.item_list), leave=False, desc=func_name) as pbar:
                for item in self.item_list:
                    try:
                        func(item)
                    except Exception as expt:
                        if self.exeptions is None:
                            self.exeptions = {}
                        exception_info = {'exeption': expt, 'item': item}
                        if func_name in self.exeptions.keys():
                            self.exeptions[func_name].append(exception_info)
                        else:
                            self.exeptions[func_name] = [exception_info]
                    pbar.update(1)
        return inner

    def print_results_per_item(self, sort=False, reverse=True, compare=False) -> None:
        num_items = len(self.item_list)
        results = self.results
        results = {func_name: (1 / results[func_name] * num_items) for func_name in results}
        results_header = ' Func name  | Items/sec'
        self._print_results(results=results, results_header=results_header, sort=sort, reverse=reverse, compare=compare)
