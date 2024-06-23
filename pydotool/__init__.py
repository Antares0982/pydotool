from typing import Callable as __Callable

import _pydotool  # type: ignore

from .ascii_2_keycode import *
from .click import *
from .input_event_code import *
from .key import *
from .mousemove import *
from .typetool import *


init: __Callable[[], None] = _pydotool.init
uinput_emit: __Callable[[int, int, int, bool], None] = _pydotool.uinput_emit
