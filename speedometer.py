import math
import time
import threading

wheel_size = 26  # move to config file
odometer = 69


def distance(r): return (wheel_size * math.pi) * r
def miles(inch): return distance(inch) / 12 / 5280  # miles
def hour(t): return t / 60 / 60  # hours
def mph(r, t): return miles(r) / hour(t)


def current_speed(revs, last, dwell, speed):
    real = mph(revs, dwell) if revs > 0 else speed
    potential = mph(1, time.time() - last)
    n = min(real, potential)
    # jump to 0 early for aesthetics
    return math.floor(n) if potential > 1.5 else 0


def update_state(state):
    revs, time, speed, odo, dwell = state
    state[0] = 0
    state[2] = current_speed(revs, time, dwell, speed)
    state[3] += miles(revs)
    return state


class Speedometer:
    def __init__(self):
        # todo: get wheel size & odo
        self.state = [0, time.time(), 0, odometer, 0]
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.stop_event = threading.Event()
        self.lock = threading.Lock()
        self.thread.start()

    def stop(self):
        # daemon threads will self terminate
        self.stop_event.set()

    def run(self):
        while not self.stop_event.is_set():
            print(self.state)
            self.state = update_state(self.state)
            time.sleep(0.1)

    def speed(self):
        return self.state[2]

    def odo(self):
        return self.state[3]

    def trigger_sensor(self):
        now = time.time()
        duration = now - self.state[1]
        print('dwell time', duration)
        self.state[0] += 1
        self.state[1] = now
        self.state[4] = duration
