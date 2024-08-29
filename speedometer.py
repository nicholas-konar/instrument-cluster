import math
import time
import threading

wheel_size = 26  # move to config file
odometer = 69
refresh_rate = 0.1


class State:
    def __init__(self):
        self.revs = 0
        self.dwell = 0
        self.speed = 0
        self.last = time.time()
        self.odo = odometer

    def __iter__(self):
        return iter(vars(self).values())

    def __repr__(self):
        return f"[{', '.join(f'{k}:{v}' for k, v in vars(self).items())}]"


def distance(r): return (wheel_size * math.pi) * r
def miles(inch): return distance(inch) / 12 / 5280  # miles
def hour(t): return t / 60 / 60  # hours
def mph(r, t): return miles(r) / hour(t)
def smooth(n, s): return n * .5 + s * .5


def current_speed(r, t, d, s):
    real = mph(r, d) if r > 0 else s
    potential = mph(1, time.time() - t)
    display = min(real, potential)
    return math.floor(display) if potential > 1.5 else 0


def update_state(state: State):
    # todo: account for multiple revolutions
    revs, dwell, speed, time, _ = state
    state.revs = 0
    state.speed = current_speed(revs, time, dwell, speed)
    state.odo += miles(revs)
    return state


class Speedometer:
    def __init__(self):
        # todo: get wheel size & odo
        self.state = State()
        self.thread = threading.Thread(target=self.start, daemon=True)
        self.stop_event = threading.Event()
        self.lock = threading.Lock()
        self.thread.start()

    def start(self):
        while not self.stop_event.is_set():
            self.state = update_state(self.state)
            time.sleep(refresh_rate)

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
