import threading
import time

from state import State
from config import read_config, write_config

config = read_config()


class Odometer:
    def __init__(self, state: State):
        self.state = state
        self.interval = config['odo_interval']
        self.thread = threading.Thread(target=self.start, daemon=True)
        self.stop_event = threading.Event()
        self.thread.start()

    def start(self):
        last = self.state.odo
        while not self.stop_event.is_set():
            if (self.state.odo > last):
                write_config({'odo_miles': self.state.odo})
                last = self.state.odo
            time.sleep(self.interval)

    def stop(self):
        # daemon threads will self terminate
        self.stop_event.set()

    def miles(self):
        return f"{self.state.odo:.2f}"
