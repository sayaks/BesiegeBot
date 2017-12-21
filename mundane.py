import asyncio
import discord
import random
import config

with open("./statuses.txt") as f:
	STATUSES = f.read().splitlines()

LOGOUT = []

LOG_CHANNEL_ID = None

messages_since_startup = 0
messages_total = 0

config.register(__name__, 'LOG_CHANNEL_ID')
config.register(__name__, 'messages_total')


async def game_status_per_message(client, message):
	if message.channel.is_private:
		client.log(
			f'Recieved message "{message.content}" from {message.author}'
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
	
async def reload(client, message):
	client.log(f"{messages_since_startup} messages since startup")
	await client.delete_message(message)
	if (client.sent_by_admin(message)):
		client.log("logging out...")
		for l in LOGOUT:
			l()
		await client.logout()
	else:
		client.log(
			"{0} ({1}) tried to reload, but was denied".format(
				message.author,
				message.author.top_role,
			)
		)

async def set_log_channel(client, message):
	await client.delete_message(message)
	if (client.sent_by_admin(message)):
		global LOG_CHANNEL_ID
		client.log(
			f"{message.author} set LOG_CHANNEL from "
			f"{client.get_channel(LOG_CHANNEL_ID)} to {message.channel}"
		)
		LOG_CHANNEL_ID = message.channel.id
	else:
		client.log(
			"{0} ({1}) tried to set log channel, but was denied".format(
				message.author,
				message.author.top_role,
			)
		)