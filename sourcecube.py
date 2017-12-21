import discord
import asyncio

import config
import mundane
import karma
import f1984

with open("./token.txt") as f:
	TOKEN = f.read()
	
with open("./god_users.txt") as f:
	GOD_USERS = f.read().splitlines()
	
DEFAULT = mundane.game_status_per_message
mundane.LOGOUT = [
	config.save,
	karma.save,
]
back_log = []

commands = [
	(lambda m: m.channel.name == 'screenshots', f1984.check_screenshot),

	(lambda m: m.content == '!reload', mundane.reload),
	(lambda m: m.content == '!set_log', mundane.set_log_channel),
	(lambda m: m.content == '!karma', karma.send_karma_score),
	
	(f1984.ip_check, f1984.remove_ip),
	(karma.check_karma_legal, karma.parse_karma),
]

client = discord.Client()

@client.event
async def on_ready():
	client.log(
		f'Logged in as\n{client.user.name}\n{client.user.id}\n------'
	)
	LOG_CHANNEL = None
	while True:
		await asyncio.sleep(5)
		if mundane.LOG_CHANNEL_ID == None:
			LOG_CHANNEL = None
		elif LOG_CHANNEL == None or LOG_CHANNEL.id != mundane.LOG_CHANNEL_ID:
			LOG_CHANNEL = client.get_channel(mundane.LOG_CHANNEL_ID)
		
		while len(back_log)>0 and LOG_CHANNEL != None:
			await client.send_message(LOG_CHANNEL, back_log.pop(0))
			await asyncio.sleep(0.2)
			
			

@client.event
async def on_message(message):
	if message.author.bot:
		return
		
	for command in commands:
		if command[0](message):
			client.log("Executing {0}".format(command[1]))
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
	client.log(
		f'Deleting message "{message.content}" '
		f'by {message.author} '
		f'in {message.channel}'
	)
	await client.__delete_message__(message)
client.__delete_message__ = client.delete_message
client.delete_message = delete_message
	
def log(s):
	print(s)
	if mundane.LOG_CHANNEL_ID != None:
		back_log.append(s)
	
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
