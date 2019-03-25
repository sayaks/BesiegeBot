import re
import asyncio
from karma import get_mentions
import time
import config

time_reg = (
	r'^(?:\s|(?:<[^>]*>))*'
	r'(?:([0-9]+):)?([0-9]+)'
	r'(?:\s|(?:<[^>]*>))*$'
)

MUTES, BANS = {}, {}
config.register(__name__, 'MUTES')
config.register(__name__, 'BANS')

async def add_mute(client, user, duration, server_id, mute_role):
	await client.add_roles(user, mute_role)
	MUTES[user.id] = (time.time()+duration, server_id, mute_role.id)
	
async def add_ban(client, user, duration, server_id):
	BANS[user.id] = (time.time()+duration, server_id)
	await client.ban(user, 0)

	
async def check_all(client):
	current_time = time.time()
	
	for user_id, (end, server_id, mute_role_id) in list(MUTES.items()):
		if current_time >= end:
			server = client.get_server(server_id)
			user = server.get_member(user_id)
			client.log(f"Unmuting {user.name}")
			for role in [i for i in user.roles if i.id == mute_role_id]:
				await client.remove_roles(user, role)
			del MUTES[user_id]
			await client.send_message(
				user, 
				f"You have been unmuted on '{server.name}'"
			)
		
	for user_id, (end, server_id) in list(BANS.items()):
		if current_time >= end:
			user = await client.get_user_info(user_id)
			server = client.get_server(server_id)
			client.log(f"Unbanning {user.name}")
			await client.unban(server, user)
			del BANS[user_id]
			if user_id in MUTES:
				del MUTES[user_id]

async def check_mute(client, message, prefix):
	await check_all(client)
	
	mentions = get_mentions(message, False)
	if len(mentions) == 0:
		client.log("Nobody mentioned, skipping output...") 
		return
		
	output = [
		f"User '{user.name}' isn't temp-muted"
		if user.id not in MUTES else
		f"User '{user.name}' has will be muted for " +
		f"{MUTES[user.id][0] - time.time()} more seconds"
		for user in mentions
	]
	await client.send_message(
		message.author,
		"\n".join(output)
	)

async def temp_ban(client, message, prefix):
	return await temp_stop(client, message, prefix, True)
	
async def temp_mute(client, message, prefix):
	return await temp_stop(client, message, prefix, False)
	
async def temp_stop(client, message, prefix, is_ban):
	word = "banned" if is_ban else "muted"

	text = message.content[len(prefix):]
	m = re.search(time_reg, text)
	if m is None:
		await client.send_message(
			message.channel,
			"Could not extract time from message.\n"+
			"Correct format is '[H:]m' padded with "+
			"either whitespace or mentions\n"
		)
		return
	
	hours = m.group(1)
	minutes = m.group(2)
	hours = 0 if hours is None else int(hours)
	minutes = 0 if minutes is None else int(minutes)
	
	total = hours+minutes
	
	hours += minutes // 60
	minutes %= 60
	days = hours // 24
	hours %= 24
	
	time_string = (
		(
			f"{days} days, " 
			if days > 1 
			else "" if days == 0 else "1 day, "
		) +
		(
			f"{hours} hours, "
			if hours > 1 
			else "" if hours == 0 else "1 hour, "
		) +
		(
			f"{minutes} minutes" 
			if minutes > 1 else "" if minutes == 0 
			else "1 minute"
		)
	).strip(", ")
	if not time_string:
		await client.send_message(
			message.channel,
			"Time needs to be bigger than zero\n"
		)
		return

	mentions = get_mentions(message, False)
	if len(mentions) == 0:
		await client.send_message(
			message.channel,
			f"Nobody {word} for {time_string}"
		)
		return
	
	server = message.server
	if is_ban:
		invite = await client.create_invite(server, max_uses=1)
			
		for user in mentions:
			await client.send_message(
				user, 
				(
					f"You have been banned on '{server.name}' for {time_string}"
					f", here is an invite for when it expires: {invite.url}\n"
				)
			)
			
			await add_ban(
				client, 
				user, 
				((days*24+hours)*60+minutes)*60, 
				server.id
			)
	else: 
		mute_role = [
			role 
			for role in message.server.roles 
			if "muted" in role.name.lower()
		][0]
		for user in mentions:
			await add_mute(
				client, 
				user, 
				((days*24+hours)*60+minutes)*60, 
				server.id,
				mute_role
			)
	
	mentions = [i.name for i in mentions]
	
	await client.send_message(
		message.channel,
		f"Users {mentions} {word} for {time_string}"
	)
	
	