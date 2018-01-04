import json
import re
import time
import asyncio
import discord

try:
    with open('karma.json') as f:
        user_data = json.load(f)
except:
    with open('karma.json','w') as f:
        user_data = {}
    
cooldown = 60.0

karma_matches = [
    "thx",
    "thank",
    "thanx",
    "thanks",
    "thankyou"
]


def save():
    with open('karma.json', 'w') as f:
        json.dump(user_data, f)


async def send_karma_score(client, message, prefix):
    data = get_data(message.author.id)
    await client.send_message(
        message.author,
        (
            f"Karma: {data['karma']}\n"
            f"Karma Given: {data['karma-given']}\n"
        )
    )


def check_karma_legal(message):
    return (
        has_thanks(message.content)
        and len(get_mentions(message, True)) > 0
        and not_on_cooldown(message.author)
    )


async def parse_karma(client, message):
    give_karma(client, message.author, get_mentions(message, True))


async def top_karma(client, message, prefix):
    mentions = get_mentions(message, False)

    if len(mentions) == 0:
        to_show = get_sorted(0)
    elif len(mentions) == 1:
        to_show = get_sorted(get_rank(mentions[0].id) - 8)
    else:
        to_show = [
            (r + 1, u.name, get_data(u.id))
            for u, r
            in zip(mentions, range(len(mentions)))
        ]

    if len(to_show) == 0:
        return

    emb = discord.Embed(
        title=f'Top Karma around rank {to_show[len(to_show)//2][0]}',
        type='rich',
        description=(
            "```js\n"
            + "Rank | User | Karma | Given\n"
            + "\n".join([
                f'[{d[0]}]\t{d[1]}:\t'
                f'{d[2]["karma"]}\t{d[2]["karma-given"]}'
                for d
                in to_show
            ])
            + "```"
        )
    )
    await client.send_message(
        message.channel,
        embed=emb)


def get_data(userid):
    data = user_data.get(
        userid,
        None,
    )
    if data == None:
        data = {
            'karma': 0,
            'karma-given': 0,
            'last-karma': None
        }
        user_data[userid] = data
    return data


def get_sorted(rank, limit=16):
    sorted_dict = sorted(
        user_data.items(),
        key=lambda i: (i[1]['karma'], i[1]['karma-given']),
        reverse=True
    )
    if len(sorted_dict) < rank + limit:
        rank = len(sorted_dict) - limit
    if rank < 0:
        rank = 0

    return [
        (r + 1 + rank, u[0], u[1])
        for u, r
        in zip(sorted_dict[rank:], range(limit))
    ]


def get_rank(userid):
    sorted_dict = sorted(
        user_data.items(),
        key=lambda i: (i[1]['karma'], i[1]['karma-given']),
    )
    for i, j in zip(range(len(sorted_dict)), sorted_dict):
        if j[0] == userid:
            return i
    return len(sorted_dict)


def has_thanks(content):
    content = content.lower()
    for m in karma_matches:
        if re.search(f"([^a-zA-Z]|^){m}([^a-zA-Z]|$)", content):
            return True
    return False


def get_mentions(message, skip_self):
    members = []
    for member in message.mentions:
        if skip_self and member == message.author:
            continue
        if member in members:
            continue
        members.append(member)
    return members


def not_on_cooldown(user):
    data = get_data(user.id)
    if data['last-karma'] == None:
        return True
    return time.time() - data['last-karma'] > cooldown


def give_karma(client, from_user, to_users):
    client.log("{0} gave karma to {1}".format(
        from_user,
        [str(to_user) for to_user in to_users]
    ))

    f = get_data(from_user.id)
    f['karma-given'] += len(to_users)
    f['last-karma'] = time.time()

    for to_user in to_users:
        t = get_data(to_user.id)
        t['karma'] += 1
