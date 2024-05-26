from typing import Any

import _pydotool  # type: ignore

from ._sequence import const_gen, sequence_call
from .input_event_code import EV_KEY


KEY_DEFAULT_DELAY = 12
_uinput_emit = _pydotool.uinput_emit

DOWN = 1
UP = 0


def key(key_code: int, is_down: bool):
    _uinput_emit(EV_KEY, key_code, DOWN if is_down else UP, True)


def key_seq(keys: "tuple[int, int] | list[tuple[int, int]]", next_delay_ms: "int | float | None" = None, delay_sequence: "list[int | float] | None" = None):
    if next_delay_ms is None and delay_sequence is None:
        next_delay_ms = KEY_DEFAULT_DELAY
    elif next_delay_ms is not None and delay_sequence is not None:
        raise ValueError("Cannot specify both next_delay_ms and delay_sequence")

    if not isinstance(keys, list):
        keys = [keys]

    if delay_sequence is not None and len(delay_sequence) < len(keys) - 1:
        raise ValueError("delay_sequence is shorter than keys")

    if delay_sequence is None:
        delays: Any = const_gen(next_delay_ms)
    else:
        delays = delay_sequence
    sequence_call(key, keys, delays)


def input_key(key_code: int, down_up_delay_ms: "int | float" = KEY_DEFAULT_DELAY):
    key_seq([(key_code, DOWN), (key_code, UP)], down_up_delay_ms)


def input_key_sequence(
        keys: "list[int]",
        down_up_delay_ms: "int | float" = KEY_DEFAULT_DELAY,
        next_key_delay_ms: "int | float" = KEY_DEFAULT_DELAY
):
    input_keys: "list[tuple[int, int]]" = sum(([(key, DOWN), (key, UP)] for key in keys), [])
    delay_sequence = [down_up_delay_ms, next_key_delay_ms] * len(input_keys)
    key_seq(input_keys, delay_sequence=delay_sequence)


def key_combination(
        keys: "list[int]",
        each_delay_ms: "int | float" = KEY_DEFAULT_DELAY,
        press_ms: "int | float" = KEY_DEFAULT_DELAY
):
    input_keys: "list[tuple[int, int]]" = [(key, DOWN) for key in keys] + [(key, UP) for key in reversed(keys)]
    delay_sequence = [each_delay_ms] * (len(keys) - 1) + [press_ms] + [each_delay_ms] * (len(keys) - 1)
    key_seq(input_keys, delay_sequence=delay_sequence)
