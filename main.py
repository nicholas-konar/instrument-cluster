import signal
import tkinter as tk

from state import State
from odometer import Odometer
from speedometer import Speedometer
from gui import gui


def main():
    def shutdown():
        speedometer.stop()
        odometer.stop()
        root.destroy()
        exit(0)

    root = tk.Tk()
    state = State()
    speedometer = Speedometer(state)
    odometer = Odometer(state)

    signal.signal(signal.SIGINT, shutdown)
    root.protocol("WM_DELETE_WINDOW", shutdown)

    gui(root, speedometer, odometer)

    root.mainloop()


if __name__ == "__main__":
    main()
