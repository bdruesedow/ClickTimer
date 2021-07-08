import sys # Imports are automatically detected (normally) in the script to freeze
import os
import cx_Freeze

base = None

os.environ["TCL_LIBRARY"] = "C:\\Python38\\tcl\\tcl8.6"
os.environ["TK_LIBRARY"] = "C:\\Python38\\tcl\\tk8.6"

if sys.platform=='win32':
    base = "Win32GUI"


executables = [cx_Freeze.Executable("timer.py", base="Win32GUI")]

cx_Freeze.setup(
        name = "ClickTimer",
        options = {"build_exe":{"packages":["sys","time","signal","tkinter","pynput"],"include_files":["C:\\Python38\\tcl\\tcl8.6", "C:\\Python38\\tcl\\tk8.6"]}},
        version="1.0",
        executables=executables)
