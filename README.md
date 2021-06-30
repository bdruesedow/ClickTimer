# ClickTimer

This is a simple application, to start a timer when a left mouse click is detected. It could be used to measure the time of a process that is initiated with a click on a button. To stop the measurement use F9 button.

## Prerequisites

* Python `>= 3.8.5` (may also work with earlier versions)
* pip `>= 21.1` (may also work with earlier version)

### Modules

```
tkinter
pynput
```

### Python Module Istallation

```bash
$ pip install tkinter
$ pip install pynput
```

## Usage

### Console

To start the application from the console:

```bash
python timer.py
```

### Standalone Windows

Note: The Standalone version for Windows do not require any Python installation on your system.

1. Download the latest release.
2. Unpack it.
3. Start `timer.exe`.


## Build the standalon windows version

```bash
python build.py build
```


## Change the Stop Button

Changing the Stop button is very simple, but needs to be done in the code by now.
Just change the Key in the following line of the method `on_press()`:

```python
if key == keyboard.Key.f9 and isTimerStarted:
```

More information of `pynput.keyboard` module here: https://pypi.org/project/keyboard/
