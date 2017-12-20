import discord
import asyncio
import random

with open("./token.txt") as f:
	TOKEN = f.read()

with open("./statuses.txt") as f:
	STATUSES = f.read().splitlines()
	
DEFAULT = None
	
commands = []
	
client = discord.Client()
messages_since_startup = 0

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
	if len(message.attachments) == 0:
		await client.delete_message(message)
		
async def game_status_per_message(message):
	global messages_since_startup
	if messages_since_startup % 1000 == 0:
		await client.change_presence(
			game=discord.Game(
				name=random.choice(STATUSES)
			)
		)
	messages_since_startup += 1
	
async def reload(message):
	client.delete_message(message)
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

commands.append((lambda m: m.channel.name == 'screenshots', check_screenshot))

commands.append((lambda m: m.content == '!reload', reload))

DEFAULT = game_status_per_message

def run():
	client.run(TOKEN)

if __name__ == "__main__":
	client.run(TOKEN)