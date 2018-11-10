with open("./token.txt") as f:
	lines = f.read().splitlines()
	DISCORD_TOKEN = lines[0]
	PLOTLY_NAME = lines[1]
	PLOTLY_TOKEN = lines[2]