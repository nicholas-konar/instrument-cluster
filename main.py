import signal
import tkinter as tk

from state import State
from gps import GPS
from odometer import Odometer
from speedometer import Speedometer
from gui import gui


def main():
    def shutdown(*args):
        gps.stop()
        speedometer.stop()
        odometer.stop()
        root.quit()
        exit(0)

    root = tk.Tk()
    state = State()
    gps = GPS(state)
    speedometer = Speedometer(state)
    odometer = Odometer(state)

    signal.signal(signal.SIGINT, shutdown)
    root.protocol("WM_DELETE_WINDOW", shutdown)

    gui(root, state, speedometer)

    root.mainloop()


if __name__ == "__main__":
    main()
