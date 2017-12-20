import discord
import asyncio
import random
import re

with open("./token.txt") as f:
	TOKEN = f.read()

with open("./statuses.txt") as f:
	STATUSES = f.read().splitlines()
	
DEFAULT = None
	
commands = []
	
client = discord.Client()
messages_since_startup = 0

ip_reg = (
	r'(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}'
	r'([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
	for command in commands:
		if command[0](message):
			print("Executing {0}".format(command[1]))
			await command[1](message)
			return
	if DEFAULT != None:
		await DEFAULT(message)

async def check_screenshot(message):
	if len(message.attachments) > 0:
		return
	for embed in message.embeds:
		if print(embed['type']) == "image":
			return
	
	await client.delete_message(message)
		
async def game_status_per_message(message):
	global messages_since_startup
	if messages_since_startup % 200 == 0:
		await client.change_presence(
			game=discord.Game(
				name=random.choice(STATUSES)
			)
		)
	messages_since_startup += 1
	
async def reload(message):
	print(f"{messages_since_startup} messages since startup")
	await client.delete_message(message)
	if message.author.top_role.id == '261519756417433601':
		print("logging out...")
		await client.logout()
	else:
		print(
			"{0} ({1}) tried to reload, but was denied".format(
				message.author,
				message.author.top_role,
			)
		)

def ip_check(message):
	if message.channel.name == "looking-to-play":
		return False
	if message.channel.name.startswith("multiverse"):
		return False
	return re.search(ip_reg, message.content) != None

async def remove_ip(message):
	await client.delete_message(message)
	await client.send_message(
		message.author, 
		(
			f"Hi, you posted your ip in {message.channel.name}, which isn't a "
			f"Multiverse channel.\nAs your god I command you to post your IP "
			f"in either #looking-to-play or a channel starting with "
			f"#multiverse.\n\nIf there was a mistake, and you didn't post "
			f"your ip, the blame lies on ITR, tell ITR that ITR did a bad"
			f"\n\t~SourceCube"
		)
	)
	
commands.append((lambda m: m.channel.name == 'screenshots', check_screenshot))

commands.append((lambda m: m.content == '!reload', reload))

commands.append((ip_check, remove_ip))

DEFAULT = game_status_per_message

def run():
	client.run(TOKEN)

if __name__ == "__main__":
	client.run(TOKEN)