#------------------------------
#RUN THIS SCRIPT TO PLAY!!!
#------------------------------
import game
from gameobject import GameObject, findByName
from lobby import lobbyMain
#from boardgamelogic import boardgameMain
import asyncio
from title import titleGo, titleMenu

async def taskMain():
	game.__init__()
	game.playerObject = GameObject("player",[game.windowDimensions[0]/2,game.windowDimensions[1]/2])
	asyncio.create_task(game.gameMain())
	await asyncio.sleep(0.1)
	#on bootup main defers to the title sequence and then suspends processing until title sequence complete
	game.gameState="title"
	while(game.programLive):
		if game.gameState=="title":
			game.frame = 0
			await titleGo()
			await titleMenu()
			await lobbyMain()
			print("done")
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