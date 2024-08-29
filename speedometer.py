import math
import time
import threading

from state import State
from config import read_config

config = read_config()
diameter = config['wheel']['diameter']
circumference = diameter * math.pi

def distance(r): return r * circumference
def miles(r): return distance(r) / 12 / 5280  # inches -> miles
def hour(t): return t / 60 / 60  # millis -> hours
def mph(r, t): return miles(r) / hour(t)
def smooth(n, s): return n * .5 + s * .5


def current_speed(r, t, d, s):
    real = mph(r, d) if r > 0 else s
    potential = mph(1, time.time() - t)
    display = min(real, potential)
    return math.floor(display) if potential > 1.5 else 0


def update_state(state: State):
    revs, dwell, speed, time, _ = state
    state.revs = 0
    state.speed = current_speed(revs, time, dwell, speed)
    state.odo += miles(revs)
    return state


class Speedometer:
    def __init__(self, state: State):
        self.state = state
        self.interval = config['speedo']['interval']
        self.thread = threading.Thread(target=self.start, daemon=True)
        self.stop_event = threading.Event()
        self.lock = threading.Lock()
        self.thread.start()

    def start(self):
        while not self.stop_event.is_set():
            self.state = update_state(self.state)
            time.sleep(self.interval)

    def stop(self):
        # daemon threads will self terminate
        self.stop_event.set()

    def speed(self):
        return self.state.speed

    def odo(self):
        return self.state.odo

    def trigger_sensor(self):
        now = time.time()
        if not self.state.revs:
            self.state.dwell = now - self.state.last
        self.state.last = now
        self.state.revs += 1
