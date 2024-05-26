
from enum import IntFlag
from typing import Any

import _pydotool  # type: ignore

from ._sequence import const_gen, sequence_call
from .input_event_code import EV_KEY


CLICK_DEFAULT_DELAY = 25

_uinput_emit = _pydotool.uinput_emit


class ClickEnum(IntFlag):
    LEFT = 0
    RIGHT = 1
    MIDDLE = 2
    SIDE = 3
    EXTR = 4
    FORWARD = 5
    BACK = 6
    TASK = 7
    MOUSE_DOWN = 0x40
    MOUSE_UP = 0x80
    MOUSE_CLICK = MOUSE_DOWN | MOUSE_UP
    LEFT_CLICK = MOUSE_CLICK | LEFT
    RIGHT_CLICK = MOUSE_CLICK | RIGHT


def _click_seq_parse(key_sequence: list[ClickEnum]) -> "list[tuple[int, int, int, int]]":
    ret = []
    for key in key_sequence:
        keycode = (key.value & 0xf) | 0x110
        if key & ClickEnum.MOUSE_DOWN:
            ret.append((EV_KEY, keycode, 1, 1))
        if key & ClickEnum.MOUSE_UP:
            ret.append((EV_KEY, keycode, 0, 1))
    return ret


def click_sequence(key_sequence: "ClickEnum | list[ClickEnum]", next_delay_ms: "int | float | None" = None, delay_sequence: "list[int | float] | None" = None):
    if next_delay_ms is None and delay_sequence is None:
        next_delay_ms = CLICK_DEFAULT_DELAY
    elif next_delay_ms is not None and delay_sequence is not None:
        raise ValueError("Cannot specify both next_delay_ms and delay_sequence")

    if not isinstance(key_sequence, list):
        key_sequence = [key_sequence]

    call_sequence = _click_seq_parse(key_sequence)
    if delay_sequence is not None and len(delay_sequence) < len(call_sequence) - 1:
        raise ValueError("delay_sequence is shorter than key_sequence")

    if next_delay_ms is not None:
        assert delay_sequence is None
        delays: Any = const_gen(next_delay_ms)
    else:
        delays = delay_sequence
    assert delays is not None
    sequence_call(_uinput_emit, call_sequence, delays)


def click(key: ClickEnum, next_delay_ms: "int | float" = CLICK_DEFAULT_DELAY):
    click_sequence([key], next_delay_ms)


def left_click(release_delay_ms=CLICK_DEFAULT_DELAY):
    click(ClickEnum.LEFT_CLICK, release_delay_ms)


def right_click(release_delay_ms=CLICK_DEFAULT_DELAY):
    click(ClickEnum.RIGHT_CLICK, release_delay_ms)


def double_click(key: ClickEnum, release_delay_ms=CLICK_DEFAULT_DELAY, gap_delay_ms=100):
    click_sequence(
        [key, key],
        delay_sequence=[release_delay_ms, gap_delay_ms, release_delay_ms]
    )


def left_double_click(release_delay_ms=CLICK_DEFAULT_DELAY, gap_delay_ms=100):
    double_click(ClickEnum.LEFT_CLICK, release_delay_ms, gap_delay_ms)


def right_double_click(release_delay_ms=CLICK_DEFAULT_DELAY, gap_delay_ms=100):
    double_click(ClickEnum.RIGHT_CLICK, release_delay_ms, gap_delay_ms)
