"""Wrapper over timeit to easy benchmark.
"""
from collections import defaultdict
from functools import partial
from timeit import timeit
from typing import Any, Callable, Dict, List, Optional, Union

from rich import print as rprint
from rich.progress import (
    BarColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)

AnyFunc = Callable[[Union[Any, None]], Union[Any, None]]


def benchmark(
    name: str,
    func: AnyFunc,
    num_repeats: int,
    progress_bar: Progress,
) -> List[float]:
    """Return list of run times for func, num_repeats times"""
    run_times: List[float] = []
    text_color = "[blue]"
    task = progress_bar.add_task(f"{text_color}{name}", total=num_repeats)
    for i in range(num_repeats):
        progress_bar.tasks[
            task
        ].description = f"{text_color}{name}: run {i + 1}/{num_repeats}"
        run_times.append(timeit(func, number=1))  # type: ignore
        progress_bar.update(task, advance=1)
    run_time_avg = sum(run_times) / len(run_times)
    progress_bar.tasks[
        task
    ].description = f"{text_color}{name}: {run_time_avg:0.2f} sec/run."
    return run_times


def get_func_name(func: AnyFunc) -> str:
    """Return name of Callable - function ot partial"""
    if isinstance(func, partial):
        args = ", ".join(
            [str(arg) for arg in func.args] + [
                f"{k}={v}" for k, v in func.keywords.items()
            ]
        )
        return f"{func.func.__name__}({args})"
    return func.__name__


class Benchmark:
    """Benchmark functions, num_repeats times"""

    _max_name_len: int = 0
    progress_bar: Progress
    _results: Dict[str, List[float]]
    func_dict: Dict[str, AnyFunc]

    def __init__(
        self,
        func: Union[AnyFunc, Dict[str, AnyFunc], List[AnyFunc]],
        num_repeats: int = 5,
        clear_progress: bool = True,
    ):
        self.num_repeats = num_repeats
        if isinstance(func, dict):
            self.func_dict = func
        elif isinstance(func, list):
            self.func_dict = {get_func_name(func_item): func_item for func_item in func}
        else:
            self.func_dict = {get_func_name(func): func}
        self._benchmark = benchmark
        self.results_header = " Func name  | Sec / run"
        self.clear_progress = clear_progress
        self._reset_results()

    def run(
        self,
        func_name: Union[str, None, List[str]] = None,
        exclude: Union[str, List[str], None] = None,
        num_repeats: Union[int, None] = None,
    ) -> None:
        """Run benchmark, can run only ones you need, exclude that you don't need"""
        if func_name:
            if isinstance(func_name, str):
                func_name = [func_name]
            func_to_test = list(set(self.func_dict).intersection(func_name))
            if len(func_name) != len(func_to_test):  # something missed
                self._print_missed(func_name)

        elif exclude:
            if isinstance(exclude, str):
                exclude = [exclude]
            func_to_test = [key for key in self.func_dict if key not in exclude]
            if len(exclude) != len(func_to_test):  # something missed
                self._print_missed(exclude)
        else:
            func_to_test = list(self.func_dict)

        self._run(func_to_test, num_repeats)

    def _print_missed(self, func_names: List[str]) -> None:
        for func in func_names:
            if func not in self.func_dict:
                rprint(f"{func} is not in func_dict")

    def _reset_results(self) -> None:
        self._results = {}  # ? if exists add new

    def _run(
        self,
        func_names: Union[List[str], Dict[str, AnyFunc]],
        num_repeats: Union[int, None] = None,
    ) -> None:
        self._reset_results()
        if len(func_names) == 0:
            rprint("Nothing to test")
        else:
            if num_repeats is None:
                num_repeats = self.num_repeats
            # func_names = func_dict.keys()
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
                    self.progress_bar.tasks[  # pylint: disable=invalid-sequence-index
                        main_task
                    ].description = (
                        f"{text_color}running {func_name} {num + 1}/{num_funcs}"
                    )
                    self._results[func_name] = self._run_benchmark(
                        func_name, num_repeats=num_repeats
                    )
                    self.progress_bar.update(main_task, advance=1)
                self.progress_bar.tasks[  # pylint: disable=invalid-sequence-index
                    main_task
                ].description = f"{text_color}done {num_funcs} runs."
                columns = self.progress_bar.columns
                self.progress_bar.columns = (
                    columns[0],
                    columns[3],
                )  # remove BarColumn and TaskProgressColumn

            self._after_run()

    def _after_run(self) -> None:
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
        """Return dict w/ results"""
        if self._results:
            return {
                name: sum(res_list) / len(res_list)
                for name, res_list in self._results.items()
            }
        return {}

    def print_results(
        self,
        results_header: Optional[str] = None,
        sort: bool = True,
        reverse: bool = False,
        compare: bool = True,
    ) -> None:
        """Print results of benchmark"""
        self._print_results(
            results=None,
            results_header=results_header,
            sort=sort,
            reverse=reverse,
            compare=compare,
        )

    def _print_results(
        self,
        results: Optional[Dict[str, float]] = None,
        results_header: Optional[str] = None,
        sort: bool = True,
        reverse: bool = False,
        compare: bool = False,
    ) -> None:
        if results_header is None:
            results_header = self.results_header
        rprint(results_header)
        if results is None:
            results = self.results
        func_names: list[str] = list(results.keys())
        if sort:
            func_names = sorted(func_names, key=results.get, reverse=reverse)  # type: ignore
        best_res = results[func_names[0]]
        for func_name in func_names:
            line = f"{func_name:12}: {results[func_name]:6.2f}"
            if compare:
                line += f" {(best_res / results[func_name]) - 1:0.1%}"
            rprint(line)

    @property
    def func_names(self) -> str:
        """Return func names as string"""
        return ", ".join(self.func_dict.keys())

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.func_names})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.func_names})"


class BenchmarkIter(Benchmark):
    """Benchmark func over item_list"""

    _num_samples: Optional[int] = None

    def __init__(
        self,
        func: Union[AnyFunc, Dict[str, AnyFunc], List[AnyFunc]],
        item_list: List[Any],
        num_repeats: int = 5,
        clear_progress: bool = True,
    ):
        super().__init__(func, num_repeats=num_repeats, clear_progress=clear_progress)
        self.item_list = item_list
        self.exceptions: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    def _run_benchmark(self, func_name: str, num_repeats: int) -> List[float]:
        return self._benchmark(
            f"{func_name:{self._max_name_len}}",
            self.run_func_iter(func_name),
            num_repeats,
            self.progress_bar,
        )

    def _reset_results(self) -> None:
        self.exceptions = defaultdict(list)
        super()._reset_results()

    def run_func_iter(self, func_name: str) -> AnyFunc:
        """Return func, that run func over item_list"""

        def inner(self=self, func_name: str = func_name):
            func = self.func_dict[func_name]
            num_samples = self._num_samples or len(self.item_list)
            task = self.progress_bar.add_task(
                f"iterating {func_name}", total=num_samples
            )
            for item in self.item_list[:num_samples]:
                try:
                    func(item)
                except Exception as excpt:  # pylint: disable=broad-except
                    exception_info = {"exception": excpt, "item": item}
                    self.exceptions[func_name].append(exception_info)
                self.progress_bar.update(task, advance=1)
            self.progress_bar.tasks[task].visible = False

        return inner

    def print_results_per_item(
        self,
        sort: bool = True,
        reverse: bool = True,
        compare: bool = False,
    ) -> None:
        """Print results per item, you can compare and sort them"""
        if self.exceptions:
            rprint(
                f"Got {len(self.exceptions)} exceptions: {', '.join(self.exceptions.keys())}."
            )
        num_items = self._num_samples or len(self.item_list)
        results = {
            func_name: (1 / result * num_items)
            for func_name, result in self.results.items()
        }
        results_header = " Func name  | Items/sec"
        self._print_results(
            results=results,
            results_header=results_header,
            sort=sort,
            reverse=reverse,
            compare=compare,
        )

    def _after_run(self) -> None:
        self.print_results_per_item()

    def __call__(
        self,
        num_repeats: Union[int, None] = None,
        num_samples: Optional[int] = None,
    ) -> None:
        """Run benchmark - `num_repeats` times, use `num_samples` or all items."""
        self._num_samples = num_samples
        super().__call__(num_repeats)
        self._num_samples = None

    def run(
        self,
        func_name: Union[str, None, List[str]] = None,
        exclude: Union[str, List[str], None] = None,
        num_repeats: Union[int, None] = None,
        num_samples: Optional[int] = None,
    ) -> None:
        self._num_samples = num_samples
        super().run(
            func_name=func_name,
            exclude=exclude,
            num_repeats=num_repeats,
        )
        self._num_samples = None
