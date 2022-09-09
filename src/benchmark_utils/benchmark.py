from timeit import timeit
from typing import Callable, Dict, List, Union

from rich.progress import Progress


def benchmark(name: str, func: Callable, num_repeats: int, progress_bar: Progress) -> List[float]:
    """Return list of run times for func, num_repeats times"""
    run_times = []
    text_color = '[blue]'
    task = progress_bar.add_task(f"{text_color}{name}", total=num_repeats)
    for i in range(num_repeats):
        progress_bar.tasks[task].description = f"{text_color}{name}: run {i + 1}/{num_repeats}"
        run_times.append(timeit(func, number=1))
        progress_bar.update(task, advance=1)
    return run_times


class Benchmark:
    """Bench func, num_repeats times"""
    def __init__(self, func: Union[Callable, Dict[str, Callable], List[Callable]], num_repeats: int = 5):
        self.num_repeats = num_repeats
        self._results = None
        self.bench_func_dict: Dict[str, Callable]
        if isinstance(func, dict):
            self.bench_func_dict = func
        elif isinstance(func, list):
            self.bench_func_dict = {fn.__name__: fn for fn in func}
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

    def _run(self, bench_func_dict: Dict[str, Callable], num_repeats: Union[int, None] = None) -> None:
        if num_repeats is None:
            num_repeats = self.num_repeats
        self._results = {}  # ? if exists add new
        func_names = bench_func_dict.keys()
        num_funcs = len(func_names)
        text_color = "[green]"
        with Progress(transient=True) as progress_bar:
            self.progress_bar = progress_bar
            main_task = self.progress_bar.add_task("starting...", total=num_funcs)
            for num, func_name in enumerate(func_names):
                self.progress_bar.tasks[main_task].description = f"{text_color}running {func_name} {num + 1}/{num_funcs}"  # noqa 501
                self._results[func_name] = self._run_benchmark(func_name, num_repeats=num_repeats)
                self.progress_bar.update(main_task, advance=1)

        self.print_results()

    def _run_benchmark(self, func_name: str, num_repeats: int):
        return self._benchmark(func_name, self.bench_func_dict[func_name], num_repeats, self.progress_bar)

    def __call__(self, num_repeats: Union[int, None] = None) -> None:
        if num_repeats is None:
            num_repeats = self.num_repeats
        self._run(self.bench_func_dict, num_repeats)

    @property
    def results(self) -> Dict[str, float]:
        if self._results is None:
            return {}
        else:
            result = {}
            for res in self._results:
                result[res] = sum(self._results[res]) / len(self._results[res])
            return result

    def print_results(self, results=None, results_header=None, sort=True, reverse=False, compare=True) -> None:
        self._print_results(results=results, results_header=None, sort=sort, reverse=reverse, compare=compare)

    def _print_results(
        self,
        results: Union[Dict[str, float], None] = None,
        results_header=None,
        sort=True,
        reverse=False,
        compare=False,
    ) -> None:
        if results_header is None:
            results_header = self.results_header
        if results is None:
            results = self.results
        print(results_header)
        func_names = list(results.keys())
        if sort:
            func_names = sorted(results, key=results.get, reverse=reverse)  # type: ignore
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
    def __init__(self, func: Union[Callable, Dict[str, Callable]], item_list: List = [], num_repeats: int = 5):
        super().__init__(func, num_repeats=num_repeats)
        self.item_list = item_list
        self.exeptions = None

    def _run_benchmark(self, func_name: str, num_repeats: int):
        return self._benchmark(func_name, self.run_func_iter(func_name), num_repeats, self.progress_bar)

    def run_func_iter(self, func_name: str) -> Callable:
        """Return func, that run func over item_list"""
        def inner(self=self, func_name=func_name):
            func = self.bench_func_dict[func_name]
            task = self.progress_bar.add_task(f"iterating {func_name}", total=len(self.item_list))
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
                self.progress_bar.update(task, advance=1)
            # self.progress_bar.remove_task(task)
            self.progress_bar.tasks[task].visible = False
        return inner

    def print_results_per_item(self, sort=False, reverse=True, compare=False) -> None:
        num_items = len(self.item_list)
        results = self.results
        results = {func_name: (1 / results[func_name] * num_items) for func_name in results}
        results_header = ' Func name  | Items/sec'
        self._print_results(results=results, results_header=results_header, sort=sort, reverse=reverse, compare=compare)
