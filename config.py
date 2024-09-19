import yaml
import os

dir = os.path.dirname(__file__)
path = os.path.join(dir, 'config.yaml')

def load_config():
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def read_config():
    return config or load_config()


def write_config(config):
    with open(path, 'w') as f:
        yaml.safe_dump({**read_config(), **config}, f)


config = load_config()
