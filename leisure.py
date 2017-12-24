import zerochan
import config
import asyncio
import discord
import re
from karma import get_mentions

OFF_TOPIC_ID = None
config.register(__name__, 'OFF_TOPIC_ID')

async def zerochan_command(client, message):
	author = message.author
	await client.delete_message(message)
	if message.channel.id == OFF_TOPIC_ID and client.sent_by_admin(message):
		content = re.split(r'(?<!\\),',message.content)
		if len(content) != 3:
			return
		
		image = zerochan.get_pic(content[0][3:].strip())
		if image != None:
			embed = discord.Embed(
				title = content[1].strip(),
				type = 'rich',
				description = content[2].strip(),
				url = image[0],
			)
			embed.set_image(url=image[1])
			await client.send_message(message.channel, embed = embed)

async def hug_command(client, message):
	author = message.author
	await client.delete_message(message)
	mentions = get_mentions(message)
	if message.channel.id == OFF_TOPIC_ID and len(mentions) > 0:
		mentioned_str = ', '.join([user.name for user in mentions])
		image = zerochan.get_pic("hug")
		if image != None:
			embed = discord.Embed(
				title = 'A heartfelt hug',
				type = 'rich',
				description = f'{message.author.name} hugged {mentioned_str}',
				url = image[0],
			)
			embed.set_image(url=image[1])
			await client.send_message(message.channel, embed = embed)
		
async def set_leisure_channel(client, message):
	await client.delete_message(message)
	if (client.sent_by_admin(message)):
		global OFF_TOPIC_ID
		client.log(
			f"{message.author} set OFF_TOPIC from "
			f"{client.get_channel(OFF_TOPIC_ID)} to {message.channel}"
		)
		OFF_TOPIC_ID = message.channel.id
	else:
		client.log(
			"{0} ({1}) tried to set leisure channel, but was denied".format(
				message.author,
				message.author.top_role,
			)
		)