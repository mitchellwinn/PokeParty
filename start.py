#------------------------------
#RUN THIS SCRIPT TO PLAY!!!
#------------------------------
import game
import asyncio
from title import titleGo, titleMenu

async def taskMain():
	game.__init__()
	await asyncio.sleep(0.1)
	asyncio.create_task(game.gameMain())
	#on bootup main defers to the title sequence and then suspends processing until title sequence complete
	print("Attempting titleGo()")
	await titleGo()
	print("Awaiting termination: press ESC")
	await titleMenu()
	while(game.programLive):
		if(game.gameState=="title"):
			await titleGo()
			await titleMenu()
		await asyncio.sleep(0)


asyncio.run(taskMain())