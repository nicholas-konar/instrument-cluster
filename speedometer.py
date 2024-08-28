import math
import time
import threading
import tkinter as tk
from tkinter import ttk
import tkintermapview
import random

wheel_size = 26  # move to config file
odometer = 69


def distance(r): return (wheel_size * math.pi) * r
def miles(inch): return distance(inch) / 12 / 5280  # miles
def hour(t): return (time.time() - t) / 60 / 60  # hours


def speed(r, t):
    return miles(r) / hour(t)


def current_speed(r, p, s):
    real = speed(r, p) if r > 0 else s
    potential = speed(1, p)
    s = min(real, potential)
    # jump to 0 early for aesthetics
    return math.floor(s) if potential > 1.8 else 0


class MockGPS:
    def __init__(self):
        # Starting coordinates (New York City)
        self.latitude = 40.7128
        self.longitude = -74.0060

    def get_location(self):
        # Simulate small changes in location
        self.latitude += random.uniform(-0.0001, 0.0001)
        self.longitude += random.uniform(-0.0001, 0.0001)
        return self.latitude, self.longitude


class SpeedometerApp:
    def __init__(self, master):
        self.master = master
        master.attributes('-fullscreen', True)
        master.title("Speedometer")

        # Create a frame for the map
        self.map_frame = ttk.Frame(master)
        self.map_frame.pack(fill=tk.BOTH, expand=True)

        # Create the map widget
        self.map_widget = tkintermapview.TkinterMapView(
            self.map_frame, width=800, height=600, corner_radius=0)
        self.map_widget.pack(fill=tk.BOTH, expand=True)

        # Initialize mock GPS
        self.gps = MockGPS()

        # [revs, prev_rev_time, current_speed, odometer]
        self.state = [0, time.time(), 0, odometer]
        self.stop_event = threading.Event()

        self.speed_label = ttk.Label(master, text="0 mph", font=("Arial", 48))
        self.speed_label.pack(pady=20)

        self.odometer_label = ttk.Label(master, text=f"Odometer: {
                                        self.state[3]:.2f} miles", font=("Arial", 24))
        self.odometer_label.pack(pady=10)

        self.speedo_thread = threading.Thread(
            target=self.speedometer, daemon=True)
        self.speedo_thread.start()

        self.update_map()

    def trigger_sensor(self):
        self.state[0] += 1

    def speedometer(self):
        while not self.stop_event.is_set():
            r, p, s, o = self.state
            self.state[0] = 0
            self.state[1] = time.time() if r > 0 else p
            self.state[2] = current_speed(r, p, s)
            self.state[3] += miles(r)

            self.speed_label.config(text=f"{self.state[2]} mph")
            self.odometer_label.config(
                text=f"Odometer: {self.state[3]:.2f}mi")

            # Update GPS coordinates
            lat, lon = self.gps.get_location()
            self.map_widget.set_position(lat, lon)

            time.sleep(0.01)

    def update_map(self):
        lat, lon = self.gps.get_location()
        self.map_widget.set_position(lat, lon)
        self.map_widget.set_zoom(15)
        self.master.after(5000, self.update_map)  # Update every 5 seconds

    def on_closing(self):
        self.stop_event.set()
        self.master.quit()


class SensorTriggerApp:
    def __init__(self, master, speedometer_app):
        self.master = master
        master.title("Sensor Trigger")

        self.speedometer_app = speedometer_app

        self.trigger_button = ttk.Button(
            master, text="Trigger Sensor", command=self.trigger_sensor)
        self.trigger_button.pack(pady=20)

    def trigger_sensor(self):
        self.speedometer_app.trigger_sensor()


def main():
    root = tk.Tk()
    speedometer_app = SpeedometerApp(root)

    # Create a separate window for the sensor trigger
    trigger_root = tk.Toplevel(root)
    trigger_app = SensorTriggerApp(trigger_root, speedometer_app)

    root.protocol("WM_DELETE_WINDOW", speedometer_app.on_closing)
    # Prevent closing the trigger window
    trigger_root.protocol("WM_DELETE_WINDOW", lambda: None)

    root.mainloop()


if __name__ == "__main__":
    main()
