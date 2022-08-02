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
	game.gameState="title"
	while(game.programLive):
		if game.gameState=="title":
			game.frame = 0
			await titleGo()
			await titleMenu()
			#print("title menu done")
			if game.lobbyThread.is_alive():
				#print("alive")
			else:
				#print("thread not alive")
			while game.lobbyThread.is_alive():
				#print("alive")
				await asyncio.sleep(game.timestep/2)
			#await boardgameMain()
			game.gameState = "title"
			game.gameObjects.clear()
			game.tryDisconnect()
			game.playerObject = GameObject("player",[game.windowDimensions[0]/2,game.windowDimensions[1]/2])
		else:
			print("gameState not title")
		await asyncio.sleep(.25)

	quit()


asyncio.run(taskMain())