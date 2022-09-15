from queue import Empty
from timeit import timeit
from typing import Any, Callable, Dict, List, Union

from rich import print
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
)


def benchmark(
    name: str, func: Callable, num_repeats: int, progress_bar: Progress
) -> List[float]:
    """Return list of run times for func, num_repeats times"""
    run_times = []
    text_color = "[blue]"
    task = progress_bar.add_task(f"{text_color}{name}", total=num_repeats)
    for i in range(num_repeats):
        progress_bar.tasks[
            task
        ].description = f"{text_color}{name}: run {i + 1}/{num_repeats}"
        run_times.append(timeit(func, number=1))
        progress_bar.update(task, advance=1)
    run_time_avg = sum(run_times) / len(run_times)
    progress_bar.tasks[
        task
    ].description = f"{text_color}{name}: {run_time_avg:0.2f} sec/run."
    return run_times


class Benchmark:
    """Bench func, num_repeats times"""

    def __init__(
        self,
        func: Union[Callable, Dict[str, Callable], List[Callable]],
        num_repeats: int = 5,
        clear_progress: bool = True,
    ):
        self.num_repeats = num_repeats
        self._results: Dict[str, List[float]] = {}
        self.func_dict: Dict[str, Callable]
        if isinstance(func, dict):
            self.func_dict = func
        elif isinstance(func, list):
            self.func_dict = {fn.__name__: fn for fn in func}
        else:
            self.func_dict = {func.__name__: func}
        self._benchmark = benchmark
        self.results_header = " Func name  | Sec / run"
        self.clear_progress = clear_progress

    def run(
        self,
        func_name: Union[str, None, List[str]] = None,
        exclude: Union[str, List[str], None] = None,
        num_repeats: Union[int, None] = None,
    ) -> None:
        if func_name:
            if isinstance(func_name, str):
                func_name = [func_name]
            func_to_test = dict(
                filter(lambda item: item[0] in func_name, self.func_dict.items())
            )
            if len(func_name) != len(func_to_test):  # something missed
                self._print_missed(func_name)

        elif exclude:
            if isinstance(exclude, str):
                exclude = [exclude]
            func_to_test = dict(
                filter(
                    lambda item: item[0] not in exclude, self.func_dict.items()
                )
            )
            if len(exclude) != len(func_to_test):  # something missed
                self._print_missed(exclude)
        else:
            func_to_test = self.func_dict

        self._run(func_to_test, num_repeats)

    def _print_missed(self, func_names: List[str]) -> None:
        for func in func_names:
            if func not in self.func_dict:
                print(f"{func} is not in func_dict")

    def _reset_results(self) -> None:
        self._results = {}  # ? if exists add new

    def _run(
        self, func_dict: Dict[str, Callable], num_repeats: Union[int, None] = None
    ) -> None:
        self._reset_results()
        if len(func_dict) == 0:
            print("Nothing to test")
        else:
            if num_repeats is None:
                num_repeats = self.num_repeats
            func_names = func_dict.keys()
            num_funcs = len(func_names)
            self._max_name_len = max(len(func_name) for func_name in func_names)
            text_color = "[green]"
            with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                TimeRemainingColumn(elapsed_when_finished=True),
                transient=self.clear_progress,
            ) as progress_bar:
                self.progress_bar = progress_bar
                main_task = self.progress_bar.add_task("starting...", total=num_funcs)
                for num, func_name in enumerate(func_names):
                    self.progress_bar.tasks[
                        main_task
                    ].description = f"{text_color}running {func_name} {num + 1}/{num_funcs}"
                    self._results[func_name] = self._run_benchmark(
                        func_name, num_repeats=num_repeats
                    )
                    self.progress_bar.update(main_task, advance=1)
                self.progress_bar.tasks[
                    main_task
                ].description = f"{text_color}done {num_funcs} runs."
                columns = self.progress_bar.columns
                self.progress_bar.columns = (
                    columns[0],
                    columns[3],
                )  # remove BarColumn and TaskProgressColumn

            self.print_results()

    def _run_benchmark(self, func_name: str, num_repeats: int) -> List[float]:
        return self._benchmark(
            f"{func_name:{self._max_name_len}}",
            self.func_dict[func_name],
            num_repeats,
            self.progress_bar,
        )

    def __call__(self, num_repeats: Union[int, None] = None) -> None:
        if num_repeats is None:
            num_repeats = self.num_repeats
        self._run(self.func_dict, num_repeats)

    @property
    def results(self) -> Dict[str, float]:
        if self._results:
            result = {}
            for res in self._results:
                result[res] = sum(self._results[res]) / len(self._results[res])
            return result
        else:
            return {}

    def print_results(
        self, results=None, results_header=None, sort=True, reverse=False, compare=True
    ) -> None:
        self._print_results(
            results=results,
            results_header=None,
            sort=sort,
            reverse=reverse,
            compare=compare,
        )

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
        return ", ".join(self.func_dict.keys())

    def __repr__(self) -> str:
        return ", ".join(self.func_dict.keys())


class BenchmarkIter(Benchmark):
    """Benchmark func over item_list"""

    def __init__(
        self,
        func: Union[Callable, Dict[str, Callable], List[Callable]],
        item_list: List[Any],
        num_repeats: int = 5,
        clear_progress: bool = True,
    ):
        super().__init__(func, num_repeats=num_repeats, clear_progress=clear_progress)
        self.item_list = item_list
        self.exceptions: Union[Dict[str, List[Dict[str, Any]]], None] = None

    def _run_benchmark(self, func_name: str, num_repeats: int) -> List[float]:
        return self._benchmark(
            f"{func_name:{self._max_name_len}}",
            self.run_func_iter(func_name),
            num_repeats,
            self.progress_bar,
        )

    def _reset_results(self) -> None:
        self.exceptions = None
        super()._reset_results()

    def run_func_iter(self, func_name: str) -> Callable:
        """Return func, that run func over item_list"""

        def inner(self=self, func_name=func_name):
            func = self.func_dict[func_name]
            task = self.progress_bar.add_task(
                f"iterating {func_name}", total=len(self.item_list)
            )
            for item in self.item_list:
                try:
                    func(item)
                except Exception as excpt:
                    if self.exceptions is None:
                        self.exceptions = {}
                    exception_info = {"exception": excpt, "item": item}
                    if func_name in self.exceptions.keys():
                        self.exceptions[func_name].append(exception_info)
                    else:
                        self.exceptions[func_name] = [exception_info]
                self.progress_bar.update(task, advance=1)
            self.progress_bar.tasks[task].visible = False

        return inner

    def print_results_per_item(self, sort=False, reverse=True, compare=False) -> None:
        if self.exceptions is not None:
            print(f"Got exceptions {len(self.exceptions)}!")
        num_items = len(self.item_list)
        results = self.results
        results = {
            func_name: (1 / results[func_name] * num_items) for func_name in results
        }
        results_header = " Func name  | Items/sec"
        self._print_results(
            results=results,
            results_header=results_header,
            sort=sort,
            reverse=reverse,
            compare=compare,
        )
