import config
import discord
import re

# unicode fe57 = 'small exclamation mark'
# unicode ff01 = 'fullwidth exclamation mark'
PREFIX = ['!', '\ufe57', '\uff01']
config.register(__name__, 'PREFIX')
if isinstance(PREFIX, str):
	PREFIX = [PREFIX]

OFF_TOPIC_ID = []
config.register(__name__, 'OFF_TOPIC_ID')
if isinstance(OFF_TOPIC_ID, str):
	OFF_TOPIC_ID = [OFF_TOPIC_ID]

listed_commands = []
admin_commands = []
commands_help = []

def register(name, command, leisure=True, admin=False, delete=True, help=''):
	admin_commands.append(name)
	commands_help.append((name, help))
	if not admin:
		listed_commands.append(name)

	def check(message):
		if message.channel.is_private and message.content.startswith(name):
			return ""
		if len(message.content) < 1:
			return None
		for i in PREFIX:
			if not message.content.startswith(i):
				continue
			#if message.content[len(i):].startswith(name):
			if re.match(f'{name}\\s.+|{name}$', message.content[len(i):]):
				return i
		return None

	async def execute(client, message):
		if delete:
			await client.delete_message(message)
		if admin:
			if not client.sent_by_admin(message):
				client.log(
					f'{message.author} (`{message.author.top_role}`) '
					f'tried to use admin-only command {name}, but was denied'
				)
				embed = discord.Embed(
					title='Username is not in the sudoers file.',
					type='rich',
					description='This incident will be reported.',
					url='https://xkcd.com/838/'
				)
				embed.set_image(
					url='https://imgs.xkcd.com/comics/incident.png'
				)
				await client.send_message(message.author, embed=embed)
				return
		
		if message.channel.name == None:
			client.log(
				f'{message.author} used command {name} in DM'
			)
		elif leisure and not message.channel.name.startswith("bot"):
			if message.channel.id not in OFF_TOPIC_ID:
				await client.send_message(
					message.author, 
					(
						f'The command {name} can only '
						f'be used in #off-topic!'
					)
				)
				return
		await command(client, message, check(message) + name)

	return (check, execute)


async def add_leisure_channel(client, message, prefix):
	global OFF_TOPIC_ID
	new_id = message.channel.id
	if new_id in OFF_TOPIC_ID:
		client.log(
			f"{message.author} tried to add OFF_TOPIC "
			f"{message.channel}, but it was already in the list"
		)
		return
	client.log(
		f"{message.author} added OFF_TOPIC channel {message.channel}"
	)
	OFF_TOPIC_ID.append(message.channel.id)
	
async def delete_leisure_channel(client, message, prefix):
	global OFF_TOPIC_ID
	old_id = message.channel.id
	if old_id not in OFF_TOPIC_ID:
		client.log(
			f"{message.author} attempted to delete OFF_TOPIC channel "
			f"{message.channel}, but it wasn't off topic"
		)
		return
		
	client.log(
		f"{message.author} deleted OFF_TOPIC channel {message.channel}"
	)
	OFF_TOPIC_ID = list(
		filter(lambda x: x != old_id, OFF_TOPIC_ID)
	)

async def add_prefix(client, message, prefix):
	global PREFIX
	new_prefix = message.content[len(prefix):].strip()
	if new_prefix in PREFIX:
		client.log(
			f"{message.author} tried to add prefix "
			f"{new_prefix}, but it was already in the list"
		)
		return
	client.log(
		f"{message.author} added prefix {new_prefix}"
	)
	PREFIX.append(new_prefix)

async def delete_prefix(client, message, prefix):
	global PREFIX
	old_prefix = message.content[len(prefix):].strip()
	if not old_prefix in PREFIX:
		client.log(
			f"{message.author} tried to remove prefix "
			f"{old_prefix}, but it was not in the list"
		)
		return
	client.log(
		f"{message.author} removed prefix {old_prefix}"
	)
	PREFIX = list(filter(lambda x: x != old_prefix, PREFIX))
	
		
	
async def list_prefix(client, message, prefix):
	global PREFIX
	await client.send_message(
		message.channel,
		f'Prefixes: {str(PREFIX)}'
	)

async def help_command(client, message, prefix):
	c = message.content.strip().split(' ')
	if len(c) == 2:
		if not client.sent_by_admin(message) and not c[1] in listed_commands:
			await client.send_message(
				message.author,
				'You don\'t have access to that command.'
			)
		elif not c[1] in [help[0] for help in commands_help]:
			await client.send_message(
				message.author,
				f'The command `{c[1]}` doesn\'t exist.'
			)
		else:
			help = [h for h in commands_help if c[1] in h[0]][0]
			await client.send_message(
				message.author,
				f'```{message.author.name}@BesiegeDiscord:~$ man {help[0]}\n{help[1]}```'
			)
	else:
		if client.sent_by_admin(message):
			commands = '\n\t'.join(admin_commands)
		else:
			commands = '\n\t'.join(listed_commands)
		await client.send_message(
			message.author,
			f'Commands:\n\t{commands}'
		)


async def test_command(client, message, prefix):
	await client.send_message(
		message.channel,
		'Pong!'
	)


async def test_rich_command(client, message, prefix):
	c = message.content.split(' ')
	emb = discord.Embed(
		title='Pong!',
		type='rich',
		description=c[1], # c[0] is ofc !pingrich. wasn't really expecting that for some reason
		colour=discord.Colour(int(c[2], 16))
	)
	await client.send_message(
		message.channel,
		embed=emb
	)
	
async def test_exception_command(client, message, prefix):
	raise Exception("This exception is exceptionally good to test with!")
