import json
import sys

cfg = json.load(open('config.json'))

registered_values = []


def register(module_name, attribute):
    module = sys.modules[module_name]
    val = cfg.get(f"{module_name}/{attribute}", module.__dict__[attribute])
    registered_values.append((module, attribute))
    module.__dict__[attribute] = val


def save():
    for value in registered_values:
        cfg[f"{value[0].__name__}/{value[1]}"] = value[0].__dict__[value[1]]

    with open('config.json', 'w') as f:
        json.dump(cfg, f)
