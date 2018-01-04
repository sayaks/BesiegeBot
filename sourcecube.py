import discord
import asyncio
import re

import config
import commands

import mundane
import karma
import f1984
import leisure

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


    commands.register(
        'reload',
        mundane.reload,
        admin=True, leisure=False,
    ),
    commands.register(
        'set_log',
        mundane.set_log_channel,
        admin=True, leisure=False,
    ),
    commands.register(
        'set_leisure',
        commands.set_leisure_channel,
        admin=True, leisure=False,
    ),

    commands.register(
        'help',
        commands.help_command,
        leisure=False,
    ),
    commands.register(
        'karma',
        karma.send_karma_score,
        leisure=False,
    ),
    commands.register(
        'topkarma',
        karma.top_karma,
    ),


    commands.register(
        'zc',
        leisure.zerochan_command,
        admin=True,
    ),
    commands.register('hug', leisure.hug_command),

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

        while len(back_log) > 0 and LOG_CHANNEL != None:
            try:
                await client.send_message(LOG_CHANNEL, back_log.pop(0))
            except Exception as e:
                print(f'Something went wrong while logging:\n{e}')
            await asyncio.sleep(1)


@client.event
async def on_message(message):
    if message.author.bot:
        return

    for command in commands:
        if command[0](message):
            content = await sanitize(message.content)
            client.log(
                f'Executing {command[1]} because of message '
                f'{content} by {message.author} in {message.channel}'
            )
#			try:
            await command[1](client, message)
#			except Exception as e:
#				client.log(
#					f'Encountered an exception while running command:\n{e}'
#				)
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
    content = await sanitize(message.content)
    client.log(
        f'Deleting message\n{content}\n'
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


async def sanitize(content):
    content = content.replace("```", "\```")
    found = set(re.findall(
        r"<@!?([0-9]*)>",
        content,
    ))
    for m in found:
        user = await client.get_user_info(m)
        content = re.sub(f'<@!?{m}>', f'@{str(user)}', content)
    return f'```{content}```'


if __name__ == "__main__":
    client.run(TOKEN)
