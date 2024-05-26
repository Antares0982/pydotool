import _pydotool  # type: ignore

from .input_event_code import EV_REL, REL_HWHEEL, REL_WHEEL, REL_X, REL_Y


_uinput_emit = _pydotool.uinput_emit

INT32_MIN = -2147483648


def mouse_move(pos: "tuple[int, int]", is_abs: bool = False):
    x, y = pos
    if is_abs:
        _uinput_emit(EV_REL, REL_X, INT32_MIN, False)
        _uinput_emit(EV_REL, REL_Y, INT32_MIN, True)
    _uinput_emit(EV_REL, REL_X, x, False)
    _uinput_emit(EV_REL, REL_Y, y, True)


def wheel_move(w_wheel: int, h_wheel: int = 0):
    _uinput_emit(EV_REL, REL_HWHEEL, h_wheel, False)
    _uinput_emit(EV_REL, REL_WHEEL, w_wheel, True)
