from tokens import PLOTLY_TOKEN as TOKEN, PLOTLY_NAME as NAME

from datetime import datetime, timedelta

from plotly.plotly import plot
from plotly.graph_objs import Heatmap
from wisdom import count_time

from plotly import tools
tools.set_credentials_file(username=NAME, api_key=TOKEN)

async def generate(client, message, prefix):
	#text = message.message[len(prefix):]
	time_sub = 10 * 60
	x_range = 6
	y_range = 24
	
	start_time = datetime.now() - timedelta(minutes=1)
	data = [
		[
			count_time(
				0,
				start_time - timedelta(seconds=time_sub*(x+x_range*y))
			)
			for x in range(x_range)
		]
		for y in range(y_range)
	]
	
	trace = Heatmap(
		z = data, 
		x = [":"+str(i)+"0" for i in range(6)],
		y = [str(i) for i in range(y_range)]
	)
	url = plot([trace], filename='heatmap', auto_open=False)
	
	
	await client.send_message(
		message.channel,
		url
	)
