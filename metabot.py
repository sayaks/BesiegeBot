import subprocess
import time

if __name__ == '__main__':
	while True:
		while True:
			subprocess.run(["git", "fetch", "--all"])
			subprocess.run(["git", "reset", "--hard", "origin/master"])
			result = subprocess.run(["python3.6", "sourcecube.py"])
			if result.returncode != 0:
				break
		time.sleep(5 * 60)
