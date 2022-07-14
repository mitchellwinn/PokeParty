#------------------------------
#RUN THIS SCRIPT TO PLAY!!!
#------------------------------
import game
import asyncio
from title import titleGo

async def taskMain():
	game.__init__()
	await asyncio.sleep(0.1)
	asyncio.create_task(game.gameMain())
	#on bootup main defers to the title sequence and then suspends processing until title sequence complete
	print("Attempting titleGo()")
	await titleGo()
	print("Awaiting termination: press ESC")
	while(game.programLive):
		await asyncio.sleep(0)


asyncio.run(taskMain())

