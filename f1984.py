import re
import asyncio

ip_reg = (
	r'(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}'
	r'([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
)


async def check_screenshot(client, message):
	if len(message.attachments) > 0:
		return
	for embed in message.embeds:
		if embed['type'] == "image":
			return

	await client.delete_message(message)


def ip_check(message):
	if message.channel.is_private:
		return False
	if message.channel.name == "looking-to-play":
		return False
	if message.channel.name.startswith("multiverse"):
		return False
	return re.search(ip_reg, message.content) != None


async def remove_ip(client, message):
	author = message.author
	await client.delete_message(message)
	await client.send_message(
		author,
		(
			f"Hi, you posted your ip in {message.channel.name}, which isn't a "
			f"Multiverse channel.\nAs your god I command you to post your IP "
			f"in either #looking-to-play or a channel starting with "
			f"#multiverse.\n\nIf there was a mistake, and you didn't post "
			f"your ip, the blame lies on ITR, tell ITR that ITR did a bad"
			f"\n\t~SourceCube"
		)
	)
