import subprocess

while True:
	subprocess.call(["git","pull","origin","master"])
	subprocess.call(["python3", "besiegebot.py"])
	