import asyncio
import discord
import random

with open("./statuses.txt") as f:
	STATUSES = f.read().splitlines()

LOGOUT = []
messages_since_startup = 0

async def game_status_per_message(client, message):
	if message.channel.is_private:
		client.log(
			f'Recieved message "{message.content}" from {message.author}'
		)
		return

	global messages_since_startup
	if messages_since_startup % 200 == 0:
		await client.change_presence(
			game=discord.Game(
				name=random.choice(STATUSES)
			)
		)
	messages_since_startup += 1
	
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