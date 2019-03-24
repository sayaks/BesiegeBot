from tokens import PLOTLY_TOKEN as TOKEN, PLOTLY_NAME as NAME

from datetime import datetime, timedelta

from plotly.plotly import plot
from plotly.graph_objs import Heatmap
from wisdom import count_time, steps

import re
from datetime import datetime, timedelta

from plotly import tools
tools.set_credentials_file(username=NAME, api_key=TOKEN)

gen_re = (
	# $1: dekamin  $2: hour  $3: day  $4: month
	r"^\s*(?:((?:deka)?min|deka|dm)|(hour|h)|(day|d)|(month|m))[_\-:.,\s]*"
	# $5: delta    $6: skip
	r"(?:([0-9]+)(?:[\s\-_:;]([0-9]+))?)?\s*$"
)

gen_pat = re.compile(gen_re)

async def generate(client, message, prefix):
	text = message.content[len(prefix):]

	match = gen_pat.match(text)
	if match == None:
		await client.send_message(
			message.channel,
			"Could not parse message"
		)
		return

	delta, skip = match.group(5,6)
	delta = 16 if delta is None else int(delta)
	skip = 0 if skip is None else int(delta)

	index = [i for i, val in enumerate(match.group(1,2,3,4)) if val is not None]

	if len(index) == 0 or index[0] != 2:
		await client.send_message(
			message.channel,
			"Not yet supported"
		)
		return

	url = gen_weekhour(skip, delta)

	await client.send_message(
		message.channel,
		url
	)

def gen_weekhour(skip, delta):
	start_time = datetime.now() - timedelta(weeks=skip+delta, hours=1)
	end_time = datetime.now() - timedelta(weeks=skip, hours=1)

	data = [
		[
			sum([
				count_time(
					1,
					start_time + timedelta(weeks=w,days=d,hours=h)
				)
				for w in range(delta)
			])
			for d in range(7)
		]
		for h in range(24)
	]


	trace = Heatmap(
		name = (
			f"Hourly per day from {start_time} ({skip+delta} weeks ago)"
			f" to {end_time} ({skip} weeks ago)"
		),
		z = data,
		x = [f"-{i} days" for i in range(6, -1, -1)],
		y = [f"-{i:02}:00" for i in range(24, 0, -1)]
	)
	url = plot([trace], filename='hours_per_day', auto_open=False)
	return url










