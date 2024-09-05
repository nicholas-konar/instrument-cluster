import time
from types import SimpleNamespace

from config import read_config

config = read_config()


class State:
    def __init__(self):
        self.revs = 0
        self.dwell = 0
        self.speed = 0
        self.last = time.time()
        self.odo = config['odo_miles']
        self.gps = SimpleNamespace(lat=None, lon=None, alt=None)


    def __iter__(self):
        return iter(vars(self).values())

    def __repr__(self):
        return f"[{', '.join(f'{k}:{v}' for k, v in vars(self).items())}]"
