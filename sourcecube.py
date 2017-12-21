import discord
import asyncio

import mundane
import karma
import f1984

with open("./token.txt") as f:
	TOKEN = f.read()
	
with open("./god_users.txt") as f:
	GOD_USERS = f.read().splitlines()
	
DEFAULT = mundane.game_status_per_message
mundane.LOGOUT = [
	karma.save,
]

commands = [
	(lambda m: m.channel.name == 'screenshots', f1984.check_screenshot),

	(lambda m: m.content == '!reload', mundane.reload),
	(lambda m: m.content == '!karma', karma.send_karma_score),
	
	(f1984.ip_check, f1984.remove_ip),
	(karma.check_karma_legal, karma.parse_karma),
]

client = discord.Client()

@client.event
async def on_ready():
    client.log('Logged in as')
    client.log(client.user.name)
    client.log(client.user.id)
    client.log('------')

@client.event
async def on_message(message):
	if message.author.bot:
		return
		
	for command in commands:
		if command[0](message):
			print("Executing {0}".format(command[1]))
			await command[1](client, message)
			return
	if DEFAULT != None:
		await DEFAULT(client, message)
		
		
async def delete_message(message):
	if message.channel.is_private:
		return
	if message.channel.name == "administration":
		return
	if message.channel.name.startswith("bot"):
		return
	print(
		f'Deleting message "{message.content}" '
		f'by {message.author} '
		f'in {message.channel}'
	)
	await client.__delete_message__(message)
client.__delete_message__ = client.delete_message
client.delete_message = delete_message
	
async def log(s):
	print(s)
client.log = log

def sent_by_admin(message):
	return (
		message.author.id in GOD_USERS
		if message.channel.is_private 
		else message.author.top_role.id == '261519756417433601'
	)
client.sent_by_admin = sent_by_admin

if __name__ == "__main__":
	client.run(TOKEN)
