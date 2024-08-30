import tkinter as tk
import tkintermapview
import random

from tkinter import ttk


def create_mock_gps():
    state = {"latitude": 40.7128, "longitude": -74.0060}

    def get_location():
        state["latitude"] += random.uniform(-0.0001, 0.0001)
        state["longitude"] += random.uniform(-0.0001, 0.0001)
        return state["latitude"], state["longitude"]
    return get_location


def gui(root, speedometer, odometer):
    get_location = create_mock_gps()

    root.geometry("400x800")
    root.title("Instruments")

    map_frame = ttk.Frame(root)
    map_frame.pack(fill=tk.BOTH, expand=True)

    map_widget = tkintermapview.TkinterMapView(
        map_frame, width=800, height=600, corner_radius=0)
    map_widget.pack(fill=tk.BOTH, expand=True)

    speed_label = ttk.Label(root, text="0 mph", font=("Arial", 48))
    speed_label.pack(pady=20)

    odometer_label = ttk.Label(
        root, text=f"Odometer: {odometer.miles()} miles", font=("Arial", 24))
    odometer_label.pack(pady=10)

    def hot_keys():
        root.bind("<r>", lambda _: speedometer.trigger_sensor())

    def update_map():
        lat, lon = get_location()
        map_widget.set_position(lat, lon)
        map_widget.set_zoom(15)
        root.after(5000, update_map)

    def update_labels():
        speed_label.config(text=f"{speedometer.speed()} mph")
        odometer_label.config(text=f"Odometer: {odometer.miles()} miles")
        root.after(100, update_labels)

    hot_keys()
    update_labels()
    update_map()
