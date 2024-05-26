# pydotool
A [ydotool](https://github.com/ReimuNotMoe/ydotool) client implemented in Python. The aim of `pydotool` is to write automation scripts in an easy way.

### Usage

* click event
* key event
* mouse move event
* type characters

### How to Use

* Install [ydotoold](https://github.com/ReimuNotMoe/ydotool). you may install it from your package manager, or build it from source.

* Install `pydotool`. `pip install python-ydotool`

* Write your automation script. Call `init` once in your program to connect to `ydotoold`

```python
import pydotool
pydotool.init()
```

If you use another ydotoold socket than the default one (`/tmp/.ydotool_socket`), you can provide it in environment variable `YDOTOOL_SOCKET`, or pass it to `init()`

```python
pydotool.init("/run/ydotoold/socket")
```

### How to Implement the Examples in [ydotool](https://github.com/ReimuNotMoe/ydotool)

Switch to tty1 (Ctrl+Alt+F1), wait 2 seconds, and type some words:

```python
import time

from pydotool import KEY_F1, KEY_LEFTALT, KEY_LEFTCTRL, key_combination, init, type_string

init()  # call only once before using pydotool

key_combination([KEY_LEFTCTRL, KEY_LEFTALT, KEY_F1])
time.sleep(2)
type_string("echo Hey guys. This is Austin.")
```

Close a window in graphical environment (Alt+F4):

```python
from pydotool import KEY_F4, KEY_LEFTALT

key_combination([KEY_LEFTALT, KEY_F4])
```

Relatively move mouse pointer to -100,100:

```python
from pydotool import mouse_move
mouse_move((100, 100))
```

Move mouse pointer to 100,100:

```python
mouse_move((100, 100), True)
```

Mouse right click:

```python
from pydotool import right_click

right_click()
```

Mouse repeating left click:

```python
from pydotool import click_sequence, ClickEnum

click_sequence([ClickEnum.LEFT_CLICK] * 5)
```

`stdin` is not natively supported, but you can implement it with python stdin.

### Advanced Usage

There is no delay in pydotool API after the last event emitted.

```python
for i in range(5):
    left_click()
    if i != 4:
        time.sleep(0.025)

# above code is equivalent to
click_sequence([ClickEnum.LEFT_CLICK] * 5)
```

Customize the delay time:

```python
# Each click event is combined with "press" and "release", so there are totally 10 ydotool events, and 9 delays between each two consecutive events.
# the 9 delays are 10ms, 20ms, ..., 90ms.
click_sequence([ClickEnum.LEFT_CLICK] * 5, delay_sequence=list(range(10, 100, 10)))
```

Complex key operations:

```python
# Ctrl+K and Ctrl+D without releasing Ctrl
key_seq([(KEY_LEFTCTRL, DOWN), (KEY_K, DOWN), (KEY_K, UP), (KEY_D, DOWN), (KEY_D, UP), (KEY_LEFTCTRL, UP)])
```

Control the press time when typing:

```python
# Type "abcde", but hold 1 sec for each character.
# Note that long press may generate more content than expected.
type_string("abcde", hold_delay_ms=1000, each_char_delay_ms=20)
# possible output: 
# aaaaaaaaaaaabbbbbbbbbbbccccccccccccddddddddddddeeeeeeeeeeee
```

Long press key combination:

```python
# Press Alt+F4 for 3 secs. Can close most of the apps. Not recommended to try this.
key_combination([KEY_LEFTALT, KEY_F4], press_ms=3000)
```

Using the low level API to send event:

```python
# directly send an event using uinput_emit()
uinput_emit(EV_REL, REL_Y, 100, True)  # move 100 in y direction
```

