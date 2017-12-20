import discord
import asyncio

with open("./token.txt") as f:
	TOKEN = f.read()

with open("./statuses.txt") as f:
	STATUSES = f.read().splitlines()
	
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
	messages_since_startup += 1
	for command in commands:
		if command[0](message):
			print("Executing {0}".format(command[1]))
			await command[1](message)
			return

async def check_screenshot(message):
	if len(message.attachments) == 0:
		await client.delete_message(message)
		
async def game_status_per_message(message):
	if messages_since_startup % 1000 == 0:
		await client.change_status(
			game=discord.Game(
				name=random.choice(STATUSES)
			)
		)
	messages_since_startup += 1

commands.append((lambda m: m.channel.name == 'screenshots', check_screenshot))

commands.append((lambda m: m.channel.name != 'bot-log', ))

client.run(TOKEN)