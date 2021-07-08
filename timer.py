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

timeString = StringVar()
buttonText = StringVar()
timeName = StringVar()


def update_label():
    if isTimerStarted:
        # Berechnen der verstrichenen Zeit
        tactual = time.perf_counter()
        timeElapsed = tactual - t0

        # Formatieren der gemessenen Zeit zur Ausgabe
        hours, rem = divmod(timeElapsed, 3600)
        minutes, seconds = divmod(rem, 60)
        formattedTime = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
        timeString.set(formattedTime)
        window.after(100, update_label)

def on_click(x, y, button, pressed):
    global isTimerStarted
    global isListening
    global t0

    # wenn linker Mausklick erkannt und der Timer noch nicht läuft, aber scharfgeschaltet ist -> Timer starten
    if pressed and button == button.left and not isTimerStarted and isListening:
        # Zeitpunkt des Mausclicks speichern
        isTimerStarted = True
        t0 = time.perf_counter()

        # Debugging ausgabe
        print('Timer gestartet... Stoppen mit F9')

        update_label()

        return

def on_press(key):
    global isTimerStarted
    global isListening
    global t0
    global t1

    # wenn F9 gedrückt und Timer läuft -> Timer anhalten und verstrichene Zeit messen und ausgeben
    if key == keyboard.Key.f9 and isTimerStarted:
        # Timer anhalten
        t1 = time.perf_counter()
        isTimerStarted = False

        # Berechnen der verstrichenen Zeit
        timeElapsed = t1 - t0

        # Formatieren der gemessenen Zeit zur Ausgabe
        hours, rem = divmod(timeElapsed, 3600)
        minutes, seconds = divmod(rem, 60)
        formattedTime = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)

        # Debugging Ausgaben
        print('Timer beendet.')
        print("Gemessene Zeit: " + formattedTime)

        # Tkinter objekte aktualisieren
        buttonText.set("Timer scharf stellen")
        timeString.set(formattedTime)

        # Listener stoppen
        listenerMouse.stop()
        listenerKeyboard.stop()
        isListening = False

        # loggen der Zeiten in ein Textfile
        try:
            f = open("time-history.txt", "a")
            if (timeName.get() != ""):
                f.write(timeName.get() + ": " + formattedTime + "\n")
            else:
                f.write("n/a: " + formattedTime + "\n")
            f.close()
        except:
            print("Fehler beim Schreiben in die Datei time-history.txt")

        return

# Listener für Maus und Tastatur initialisieren
listenerMouse = mouse.Listener(on_click=on_click)
listenerKeyboard = keyboard.Listener(on_press=on_press)

def on_listenerButton_click():
    global isListening
    global newLabel
    global listener

    # wenn Timer noch nicht scharf -> scharf stellen
    if not isListening:
        isListening = True

        # Aktualisieren der Tkinter Objekte
        buttonText.set("Timer scharf")
        timeString.set("00:00:00.00")

        # Listener initialisieren
        listenerMouse = mouse.Listener(on_click=on_click)
        listenerKeyboard = keyboard.Listener(on_press=on_press)

        # Listener starten
        listenerMouse.start()
        listenerKeyboard.start()

    return

def signal_handler(sig, frame):
    listenerMouse.stop()
    listenerKeyboard.stop()
    sys.exit(0)


# register the interrupt handler for SIGINT signal (e.g.: Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

timeNameLabel = tk.Label(window, text="Name der Messung:", font=('Helvetica', 12))
timeNameLabel.place(relx=0.5, rely=0.15, anchor=tk.CENTER)

timeName = tk.Entry(window, font=('Helvetica', 12))
timeName.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

timeString.set("00:00:00.00")
timeLabel = tk.Label(window, textvariable=timeString, font=('Helvetica', 25))
timeLabel.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

buttonText.set("Timer scharf stellen")
listenerButton = tk.Button(window, textvariable=buttonText, command=on_listenerButton_click, font=('Helvetica', 12))
listenerButton.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

infoLabel1 = tk.Label(window, text="1. Timer scharf stellen", font=('Helvetica', 10))
infoLabel2 = tk.Label(window, text="2. mit Linksklick starten", font=('Helvetica', 10))
infoLabel3 = tk.Label(window, text="3. mit F9 stoppen", font=('Helvetica', 10))
infoLabel1.place(rely=0.83, anchor=tk.W);
infoLabel2.place(rely=0.89, anchor=tk.W);
infoLabel3.place(rely=0.95, anchor=tk.W);

window.mainloop()
