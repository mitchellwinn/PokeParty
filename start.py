#------------------------------
#RUN THIS SCRIPT TO PLAY!!!
#------------------------------
import game
from gameobject import GameObject, findByName
#from boardgamelogic import boardgameMain
import asyncio
from title import titleGo, titleMenu

async def taskMain():
	game.__init__()
	game.playerObject = GameObject("player",[game.windowDimensions[0]/2,game.windowDimensions[1]/2])
	await asyncio.sleep(0.1)
	asyncio.create_task(game.gameMain())
	#on bootup main defers to the title sequence and then suspends processing until title sequence complete
	print("Attempting titleGo()")
	await titleGo()
	print("Awaiting termination: press ESC")
	await titleMenu()
	while(game.programLive):
		if game.gameState=="title":
			game.frame = 0
			await titleGo()
			await titleMenu()
			#await boardgameMain()

		await asyncio.sleep(0)
	quit()


asyncio.run(taskMain())