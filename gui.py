import tkinter as tk
import tkintermapview

from tkinter import Tk, ttk
from speedometer import Speedometer
from state import State


def gui(root: Tk, state: State, speedometer: Speedometer):
    root.geometry("400x800")
    root.title("Instruments")

    map_frame = ttk.Frame(root)
    map_frame.pack(fill=tk.BOTH, expand=True)

    map_widget = tkintermapview.TkinterMapView(
        map_frame, width=800, height=600, corner_radius=0)
    map_widget.pack(fill=tk.BOTH, expand=True)

    waiting_label = ttk.Label(map_frame, text="Acquiring location...",
                              font=("Arial", 14), background="white")
    waiting_label.place(relx=0.5, rely=0.5, anchor="center")

    speed_label = ttk.Label(root, text="0 mph", font=("Arial", 48))
    speed_label.pack(pady=20)

    odometer_label = ttk.Label(
        root, text=f"Odometer: {state.odo:.2f} miles", font=("Arial", 24))
    odometer_label.pack(pady=10)

    def hot_keys():
        root.bind("<r>", lambda _: speedometer.trigger_sensor())

    def update_map():
        lat, lon = state.gps.lat, state.gps.lon
        if lat and lon:
            map_widget.set_position(lat, lon)
            map_widget.set_zoom(15)
            waiting_label.place_forget()
            print('location aquired')
        else:
            map_widget.delete_all_marker()
            waiting_label.place(relx=0.5, rely=0.5, anchor="center")
            print('aquiring location')
        root.after(5000, update_map)

    def update_labels():
        speed_label.config(text=f"{state.speed} mph")
        odometer_label.config(text=f"Odometer: {state.odo:.2f} miles")
        root.after(100, update_labels)

    hot_keys()
    update_labels()
    update_map()
