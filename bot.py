import asyncio
import json
import aiohttp

TOKEN = None
URL = 'https://discordapp.com/api'
HANDLER = {}
DEFAULT_HANDLER = None

with open("./token.txt") as f:
	TOKEN = f.read()
	
last_sequence = ""

defaults = {
	"headers": {
		"Authorization": f"Bot {TOKEN}",
		"User-Agent": "dBot (https://medium.com/@greut, 0.1)"
	}
}


async def main():
	"""Main program."""
	response = await api_call("/gateway")
	await start_session(response['url'])
	
async def api_call(path, method="GET", **kwargs):
	"""Return the JSON body of a call to Discord REST API."""
	
	kwargs = dict(defaults, **kwargs)
	
	with aiohttp.ClientSession() as session:
		async with session.get(f"{URL}{path}") as response:
			assert 200 == response.status, response.reason
			return await response.json()
			
			
async def start_session(url):
	with aiohttp.ClientSession() as session:
		async with session.ws_connect(f"{url}?v=6&encoding=json") as ws:
			async for msg in ws:
				await handle_message(msg, ws)

				
async def handle_message(msg, ws):
	data = json.loads(msg.data)

	if data["op"] == 10:  # Hello
		await ws.send_json({
			"op": 2,  # Identify
			"d": {
				"token": TOKEN,
				"properties": {},
				"compress": False,
				"large_threshold": 250
			}
		})
		asyncio.ensure_future(heartbeat(
			ws,
			data['d']['heartbeat_interval']))
	elif data["op"] == 11:  # Heartbeat ACK
		pass
	elif data["op"] == 0:  # Dispatch
		last_sequence = data['t']
		l = HANDLER.get(data['t'], DEFAULT_HANDLER)
		if l != None:
			await l(data['t'], data['d'])
	else:
		print("Unknown OP {0}".format(data["op"]))
			
async def heartbeat(ws, interval):
	"""Send every interval ms the heatbeat message."""
	while True:
		await asyncio.sleep(interval / 1000)  # seconds
		await ws.send_json({
			"op": 1,  # Heartbeat
			"d": last_sequence
		})

async def send_message(recipient_id, content):
	"""Send a message with content to the recipient_id."""
	print("Hi")
	channel = await api_call(
		"/users/@me/channels", 
		"POST",
		json={"recipient_id": recipient_id}
	)
	print("Hello")
	print(channel)
	return await api_call(
		f"/channels/{channel['id']}/messages",
		"POST",
		json={"content": content}
	)

def run():
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
	loop.close()

if __name__ == "__main__":
	run()
