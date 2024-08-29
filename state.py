import time

from config import read_config

config = read_config()

class State:
    def __init__(self):
        self.revs = 0
        self.dwell = 0
        self.speed = 0
        self.last = time.time()
        self.odo = config['odo']['mi']

    def __iter__(self):
        return iter(vars(self).values())

    def __repr__(self):
        return f"[{', '.join(f'{k}:{v}' for k, v in vars(self).items())}]"
