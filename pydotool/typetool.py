
from .ascii_2_keycode import ASCII_2_KEYCODE_MAP, FLAG_UPPERCASE
from .input_event_code import KEY_LEFTSHIFT
from .key import key_seq


HOLD_DEFAULT_DELAY = 20
TYPE_DEFAULT_DELAY = 20


def _to_call_arg(
    key_def: int,
    call_arg_seq: "list[tuple[int, int]]",
    delay_seq: "list[int|float]",
    hold_delay_ms: "int|float",
    each_char_delay_ms: "int|float",
):
    if key_def == -1:
        return
    key_code = key_def & 0xffff
    upper = bool(key_def & FLAG_UPPERCASE)
    if upper:
        call_arg_seq.append((KEY_LEFTSHIFT, True))
        delay_seq.append(0)
    call_arg_seq.append((key_code, True))
    delay_seq.append(hold_delay_ms)
    call_arg_seq.append((key_code, False))
    if upper:
        delay_seq.append(0)
        call_arg_seq.append((KEY_LEFTSHIFT, False))
    delay_seq.append(each_char_delay_ms)


def type_string(
        s: str,
        hold_delay_ms: "int | float" = HOLD_DEFAULT_DELAY,
        each_char_delay_ms: "int | float" = TYPE_DEFAULT_DELAY,
):
    try:
        type_command_seq = [ASCII_2_KEYCODE_MAP[ord(c)] for c in s]
    except IndexError:
        raise ValueError("Only ASCII characters are supported")
    call_seq: "list[tuple[int, int]]" = []
    delay_seq: "list[int | float]" = []
    for key_def in type_command_seq:
        _to_call_arg(key_def, call_seq, delay_seq, hold_delay_ms, each_char_delay_ms)
    key_seq(call_seq, delay_sequence=delay_seq)
