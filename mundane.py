import asyncio
import discord
import random
import config

with open("./statuses.txt") as f:
    STATUSES = f.read().splitlines()

LOGOUT = []

LOG_CHANNEL_ID = None

messages_since_startup = 0
messages_total = 0

config.register(__name__, 'LOG_CHANNEL_ID')
config.register(__name__, 'messages_total')


async def game_status_per_message(client, message):
    if message.channel.is_private:
        client.log(
            f'Recieved message "{message.content}" from {message.author}'
        )
        return

    global messages_since_startup, messages_total
    if messages_since_startup % 200 == 0:
        await client.change_presence(
            game=discord.Game(
                name=random.choice(STATUSES)
            )
        )
    messages_since_startup += 1
    messages_total += 1


async def reload(client, message, prefix):
    client.log(f"{messages_since_startup} messages since startup")
    client.log("logging out...")
    for l in LOGOUT:
        l()
    await client.logout()


async def set_log_channel(client, message, prefix):
    global LOG_CHANNEL_ID
    client.log(
        f"{message.author} set LOG_CHANNEL from "
        f"{client.get_channel(LOG_CHANNEL_ID)} to {message.channel}"
    )
    LOG_CHANNEL_ID = message.channel.id
