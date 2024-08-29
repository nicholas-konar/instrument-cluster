import threading
import time

from state import State
from config import read_config, write_config

config = read_config()


class Odometer:
    def __init__(self, state: State):
        self.state = state
        self.interval = config['odo']['interval']
        self.thread = threading.Thread(target=self.auto_save, daemon=True)
        self.stop_event = threading.Event()
        self.thread.start()

    def auto_save(self):
        while not self.stop_event.is_set():
            write_config({'odo': {'mi': self.state.odo}})
            time.sleep(self.interval)

    def stop(self):
        # daemon threads will self terminate
        self.stop_event.set()
