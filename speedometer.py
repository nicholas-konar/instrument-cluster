import math
from numbers import Number
import time
import threading

wheel_size = 26  # move to config file
odometer = 69


def distance(r): return (wheel_size * math.pi) * r
def miles(inch): return distance(inch) / 12 / 5280  # miles
def hour(t): return (time.time() - t) / 60 / 60  # hours
def mph(r, t): return miles(r) / hour(t)


def current_speed(r, t, s):
    real = mph(r, t) if r > 0 else s
    potential = mph(1, t)
    n = min(real, potential)
    # jump to 0 early for aesthetics
    return math.floor(n) if potential > 1.5 else 0


def update_state(state):
    r, t, s, o = state
    state[0] = 0
    state[2] = current_speed(r, t, s)
    state[3] += miles(r)
    return state


class Speedometer:
    def __init__(self):
        # todo: get wheel size & odo
        self.state = [0, time.time(), 0, odometer]
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.stop_event = threading.Event()
        self.lock = threading.Lock()
        self.thread.start()

    def stop(self):
        # daemon threads will self terminate
        self.stop_event.set()

    def run(self):
        while not self.stop_event.is_set():
            with self.lock:
                print(self.state)
                self.state = update_state(self.state)
                time.sleep(0.1)

    def speed(self):
        return self.state[2]

    def odo(self):
        return self.state[3]

    def trigger_sensor(self):
        t = time.time()
        self.state[0] += 1
        self.state[1] = t
