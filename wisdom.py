import sqlite3
from datetime import datetime

steps = [
	("Dekamin", lambda dt: dt.replace(minute = 10*(dt.minute//10), second = 0, microsecond=0)),
	("Hour", lambda dt: steps[0][1](dt.replace(minute = 0))),
	("Day", lambda dt: steps[1][1](dt.replace(hour = 0))),
	("Month", lambda dt: steps[2][1](dt.replace(day = 1))),
]


wisdomdatabase = sqlite3.connect('wisdom.db', detect_types=sqlite3.PARSE_DECLTYPES)
wcursor = wisdomdatabase.cursor()

for name, _ in steps:
	wcursor.executescript(f"""
		CREATE TABLE if not exists {name}(
			accountId text,
			time timestamp,
			messages unsigned big int NOT NULL,
			PRIMARY KEY (accountId, time)
		);
	""")

wisdomdatabase.commit()

latest = [l(datetime.now()) for _, l in steps]

def addmessage(id):
	for name, l in steps:
		now = datetime.now()
		now = l(now)
		
		wcursor.execute(
			f'SELECT accountId, time, messages FROM {name}\n'
			f'where accountId=? and time=?;\n',
			(id,now)
		)
		current = wcursor.fetchone()
		wcursor.execute(
			f'SELECT accountId, time, messages FROM {name}\n'
		)
		current = (
			(id,now,1)
			if current==None 
			else (current[0], current[1], current[2]+1)
		)

		wcursor.execute(
			f'INSERT OR REPLACE INTO {name}\n'
			f'(accountId, time, messages)\n'
			f'VALUES (?, ?, ?);',
			current
		)
	
def save():
	wisdomdatabase.commit()