import sys, signal, time
import tkinter as tk
from tkinter import StringVar, IntVar
from pynput import mouse
from pynput import keyboard

isTimerStarted = False
isListening = False
t0 = 0
t1 = 0

window=tk.Tk()
window.title("ClickTimer")
window.geometry("300x300")

status = StringVar()
buttonText = StringVar()

def on_click(x, y, button, pressed):
    global isTimerStarted
    global isListening
    global t0

    if pressed and button == button.left and not isTimerStarted and isListening:
        isTimerStarted = True
        t0 = time.perf_counter()
        print('Timer gestartet... Stoppen mit F9')
        status.set("Timer gestartet... Stoppen mit F9")
        return

def on_press(key):
    global isTimerStarted
    global isListening
    global t0
    global t1

    if key == keyboard.Key.f9 and isTimerStarted:
        t1 = time.perf_counter()
        isTimerStarted = False
        timeElapsed = t1 - t0
        hours, rem = divmod(timeElapsed, 3600)
        minutes, seconds = divmod(rem, 60)
        print('Timer beendet.')
        timeString = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
        print("Gemessene Zeit: " + timeString)
        status.set("Gemessene Zeit: " + timeString)
        buttonText.set("Timer scharf stellen")
        listenerMouse.stop()
        listenerKeyboard.stop()
        isListening = False
        try:
            f = open("time-history.txt", "a")
            f.write(timeString + "\n")
            f.close()
        except:
            print("Fehler beim Schreiben in die Datei time-history.txt")

        return

listenerMouse = mouse.Listener(on_click=on_click)
listenerKeyboard = keyboard.Listener(on_press=on_press)

def on_listenerButton_click():
    global isListening
    global newLabel
    global listener
    if not isListening:
        isListening = True
        status.set("Timer startet mit Linksklick")
        buttonText.set("Timer scharf")
        listenerMouse = mouse.Listener(on_click=on_click)
        listenerKeyboard = keyboard.Listener(on_press=on_press)
        listenerMouse.start()
        listenerKeyboard.start()
        return
    if isListening and not isTimerStarted:
        isListening = False
        buttonText.set("Timer scharf stellen")
        return

def signal_handler(sig, frame):
    listenerMouse.stop()
    listenerKeyboard.stop()
    sys.exit(0)

# register the interrupt handler for SIGINT signal (e.g.: Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

status.set("Timer aus")
newlabel = tk.Label(window, textvariable=status, font=('Helvetica', 12))
newlabel.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

buttonText.set("Timer scharf stellen")
listenerButton = tk.Button(window, textvariable=buttonText, command=on_listenerButton_click, font=('Helvetica', 12))
listenerButton.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

window.mainloop()
