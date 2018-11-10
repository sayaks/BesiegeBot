import mundane
import time


save_interval = 10 * 60
next_save = time.time() + save_interval

log_interval = 2.25 * 60 * 60
next_logged_save = 0
unlogged_saves = 0

def save_if_needed(client):
	global next_save, next_logged_save, unlogged_saves
	if time.time() >= next_save:
		next_save = time.time() + save_interval
		mundane.save_all()
		
		if time.time() > next_logged_save:
			next_logged_save = time.time() + log_interval
			if unlogged_saves > 0:
				client.log(
					f'Executed regular save at interval:\n'
					f'({unlogged_saves} unlogged saves)'
				)
				unlogged_saves = 0
			else:
				client.log(
					f'Executed regular save at interval'
				)
		else:
			unlogged_saves += 1

		
async def force_save(client, message, prefix):
	global next_save
	next_save = time.time() + save_interval
	mundane.save_all()
	client.log(
		f'Executed forced save'
	)
	
	
