import config
import discord

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
        return message.content.startswith(PREFIX + name)

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
        if leisure:
            if message.channel.id != OFF_TOPIC_ID:
                return
        await command(client, message, PREFIX + name)

    return (check, execute)


async def set_leisure_channel(client, message, prefix):
    global OFF_TOPIC_ID
    client.log(
        f"{message.author} set OFF_TOPIC from "
        f"{client.get_channel(OFF_TOPIC_ID)} to {message.channel}"
    )
    OFF_TOPIC_ID = message.channel.id


async def help_command(client, message, prefix):
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
    c = str.split(message.content, ' ')
    emb = discord.Embed(
        title='Pong!',
        type='rich',
        description=c[0],
        colour=discord.Colour(int(c[1], 16))
    )
    await client.send_message(
        message.channel,
        embed=emb
    )
