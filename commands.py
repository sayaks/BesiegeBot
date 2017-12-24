import config


PREFIX = '!'
config.register(__name__, 'PREFIX')

OFF_TOPIC_ID = None
config.register(__name__, 'OFF_TOPIC_ID')


listed_commands = []
admin_commands = []

def register(name, command, leisure=True, admin=False, delete=True):
	admin_commands.append(name)
	if not admin:
		listed_commands.append(name)

	def check(message):
		if message.channel.is_private and message.content.startswith(name):
			return True
		return message.content.startswith(PREFIX+name)
	
	async def execute(client, message):
		if delete:
			await client.delete_message(message)
		if admin:
			if not client.sent_by_admin(message):
				client.log(
					f'{message.author} ({message.author.top_role.name}) '
					f'tried to use admin-only command {name}, but was denied'
				)
				return
		if leisure:
			if message.channel.id != OFF_TOPIC_ID:
				return
		await command(client, message, PREFIX+name)
	
	
	return (check,execute)
	

async def set_leisure_channel(client, message, prefix):
	global OFF_TOPIC_ID
	client.log(
		f"{message.author} set OFF_TOPIC from "
		f"{client.get_channel(OFF_TOPIC_ID)} to {message.channel}"
	)
	OFF_TOPIC_ID = message.channel.id