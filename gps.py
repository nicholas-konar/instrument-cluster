import gpsd
import time
import threading

from state import State
from config import read_config

config = read_config()

class GPS:
    def __init__(self, state: State):
        self.state = state
        self.interval = config['gps_interval']
        self.thread = threading.Thread(target=self.start, daemon=True)
        self.stop_event = threading.Event()
        self.lock = threading.Lock()
        self.thread.start()

    def start(self):
        gpsd.connect()
        while not self.stop_event.is_set():
            try:
                packet = gpsd.get_current()

                # Mode indicates status of GPS reception
                # 0=no data, 1=no fix, 2=2D fix, 3=3D fix
                if packet.mode >= 2:
                    print('GPS Fixed!', packet.lat, packet.lon, packet.alt)
                    self.state.gps.fix = True
                    self.state.gps.lat = packet.lat
                    self.state.gps.lon = packet.lon
                    self.state.gps.alt = packet.alt
                else:
                    self.state.gps.fix = False

            except Exception as e:
                print(f"GPS Error: {e}")

            time.sleep(self.interval)

    def stop(self):
        # daemon threads will self terminate
        self.stop_event.set()

