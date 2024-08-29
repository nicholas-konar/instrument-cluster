import signal
import tkinter as tk

from state import State
from odometer import Odometer
from speedometer import Speedometer
from user_interface import create_dashboard, control_panel

def main():
    def shutdown():
        speedometer.stop()
        odometer.stop()
        root.destroy()
        exit(0)

    signal.signal(signal.SIGINT, shutdown)

    root = tk.Tk()
    state = State()
    speedometer = Speedometer(state)
    odometer = Odometer(state)

    create_dashboard(root, speedometer, odometer)

    ctrl_panel_root = tk.Toplevel(root)
    control_panel(ctrl_panel_root, speedometer)

    root.protocol("WM_DELETE_WINDOW", shutdown)
    ctrl_panel_root.protocol("WM_DELETE_WINDOW", lambda: None)

    root.mainloop()


if __name__ == "__main__":
    main()
