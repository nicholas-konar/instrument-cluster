import yaml


def load_config():
    with open('config.yaml') as f:
        return yaml.safe_load(f)


config = load_config()


def read_config():
    return config or load_config()


def write_config(config):
    with open('config.yaml', 'w') as f:
        yaml.safe_dump({**read_config(), **config}, f)
