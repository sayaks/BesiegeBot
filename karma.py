import json
import re
import time

user_data = json.load(open('karma.json'))

cooldown = 60.0

karma_matches = [
	"thx",
	"thank",
	"thanx",
	"thanks",
	"thankyou",
]

def get_data(user):
	data = user_data.get(
		user.id, 
		None,
	)
	if data == None:
		data = {
			'karma': 0,
			'karma-given': 0,
			'last-karma': None,
		}
		user_data[user.id] = data
	return data
	
	

def has_thanks(content):
	for m in karma_matches:
		if re.search(f"([^a-zA-Z]|^){m}([^a-zA-Z]|$)", content):
			return True
	return False

def not_on_cooldown(user):
	data = get_data(user)
	if data['last-karma'] == None:
		return True
	return time.time()-data['last-karma'] > cooldown

def get_mentions(message):
	members = []
	for member in message.mentions:
		if member == message.author or member in members:
			continue
		members.append(member)
	return members
	
def give_karma(from_user, to_users):
	print("{0} gave karma to {1}".format(
		from_user,
		[ str(to_user) for to_user in to_users ],
	))

	f = get_data(from_user)
	f['karma-given'] += len(to_users)
	f['last-karma'] = time.time()

	for to_user in to_users:
		t = get_data(to_user)
		t['karma'] += 1
	
def check_karma_legal(message):
	return 	(
			has_thanks(message.content)
		and len(get_mentions(message)) > 0
		and not_on_cooldown(message.author)
	)
	
def save():
	with open('karma.json', 'w') as f:
		json.dump(user_data, f)
