import mundane
import time


save_interval = 60*60*2.5
next_save = time.time() + save_interval


def save_if_needed(client):
	global next_save
	if time.time() >= next_save:
		next_save = time.time() + save_interval
		mundane.save_all()
		client.log(
			f'Executed regular save at interval'
		)

		
async def force_save(client, message, prefix):
	global next_save
	next_save = time.time() + save_interval
	mundane.save_all()
	client.log(
		f'Executed forced save'
	)
	
	
