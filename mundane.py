import asyncio
import discord
import random
import config

with open("./statuses.txt") as f:
	STATUSES = f.read().splitlines()

SAVE = []

LOG_CHANNEL_ID = None

messages_since_startup = 0
messages_total = 0

config.register(__name__, 'LOG_CHANNEL_ID')
config.register(__name__, 'messages_total')


async def game_status_per_message(client, message):
	if message.channel.is_private:
		sanitized = await client.sanitize(message.content)
		client.log(
			f'Recieved message {sanitized} from {message.author}'
		)
		return

	global messages_since_startup, messages_total
	if messages_since_startup % 200 == 0:
		await client.change_presence(
			game=discord.Game(
				name=random.choice(STATUSES)
			)
		)
	messages_since_startup += 1
	messages_total += 1


async def reload(client, message, prefix):
	client.exiting = True
	client.log(f"{messages_since_startup} messages since startup")
	client.log("logging out in 15 seconds...")
	save_all()
	await asyncio.sleep(15)
	await client.logout()
	
def save_all():
	for l in SAVE:
		l()
		
async def set_log_channel(client, message, prefix):
	global LOG_CHANNEL_ID
	client.log(
		f"{message.author} set LOG_CHANNEL from "
		f"{client.get_channel(LOG_CHANNEL_ID)} to {message.channel}"
	)
	LOG_CHANNEL_ID = message.channel.id


async def do_raise_error(client, message, prefix):
	raise Exception("Test Exception")
