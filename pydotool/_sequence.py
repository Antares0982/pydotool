import time
from itertools import islice
from typing import Callable, Generator, Iterable, TypeVar


_T = TypeVar("_T")


def sequence_call(func: Callable, args_list: "list", delay_list: "Iterable[int | float]"):
    for args, delay in zip(args_list, islice(delay_list, len(args_list) - 1)):
        func(*args)
        time.sleep(delay / 1000.)
    func(*args_list[-1])


def const_gen(const: _T) -> Generator[_T, None, None]:
    while True:
        yield const
