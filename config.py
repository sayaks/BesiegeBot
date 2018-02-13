import json
import sys

try:
	with open('config.json', 'w') as f:
		cfg = json.load(f)
except:
	cfg = {}
registered_values = []


def register(module_name, attribute):
	module = sys.modules[module_name]
	name = f'{module_name}/{attribute}'
	val = cfg.get(name, module.__dict__[attribute])
	registered_values.append((module, attribute))
	module.__dict__[attribute] = val


def save():
	for value in registered_values:
		name = f'{value[0].__name__}/{value[1]}'
		cfg[name] = value[0].__dict__[value[1]]

	with open('config.json', 'w') as f:
		json.dump(cfg, f)
