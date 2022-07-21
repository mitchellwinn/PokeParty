import game
import asyncio
import random
from gameobject import GameObject, findByName
from sprite import Sprite
from text import Text
from audio import playSound, playMusic, stopMusic

async def join():
	global inputIP
	inputIP = ""
	inputDone = False
	stopMusic()
	await asyncio.sleep(.25)
	playMusic("NBtown.mp3")
	game.gameObjects.append(GameObject("titleText",[game.windowDimensions[0]/2,game.windowDimensions[1]/2.2]))
	findByName("titleText").addComponent(Text("HOST Address:","pokemon1.ttf"),"text")
	game.gameObjects.append(GameObject("titleText2",[game.windowDimensions[0]/2,game.windowDimensions[1]/1.8]))
	findByName("titleText2").addComponent(Text("","pokemon1.ttf"),"text")
	blinker = " "
	i=0
	while inputDone==False:
		if game.playerInputs[9]==True:
			stopMusic()
			playSound("SFX_PRESS_AB.wav")
			game.gameState = "title"
			game.gameObjects.clear()
			return
		findByName("titleText2").getNamedComponent("text").text = inputIP+blinker
		i+=1
		if i>60:
			i=0
		if i>=30:
			blinker = "l"
		elif i>=0:
			blinker = " "
		await asyncio.sleep(game.timestep)

async def host():
	global inputIP,ready
	ready = False
	inputIP = ""
	inputDone = False
	stopMusic()
	await asyncio.sleep(.25)
	playMusic("NBtown.mp3")
	game.gameObjects.append(GameObject("titleText",[game.windowDimensions[0]*.175,game.windowDimensions[1]*.35]))
	findByName("titleText").addComponent(Text("Waiting for players","pokemon1.ttf",16,"left"),"text")
	game.gameObjects.append(GameObject("titleText2",[game.windowDimensions[0]/2,game.windowDimensions[1]*.5]))
	findByName("titleText2").addComponent(Text("Press 'R' to READY","pokemon1.ttf"),"text")
	game.gameObjects.append(GameObject("titleText3",[game.windowDimensions[0]/2,game.windowDimensions[1]*.65]))
	findByName("titleText3").addComponent(Text("Not all players are READY","pokemon1.ttf"),"text")
	blinker = " "
	i=0
	while inputDone==False:
		if game.playerInputs[9]==True:
			stopMusic()
			playSound("SFX_PRESS_AB.wav")
			game.gameState = "title"
			game.gameObjects.clear()
			return
		if ready==False:
			findByName("titleText2").getNamedComponent("text").text = "Press 'R' to READY"
		else:
			findByName("titleText2").getNamedComponent("text").text = "READY!"
		await asyncio.sleep(game.timestep)
		i+=1
		if i>60:
			i=0
		if i>=40:
			findByName("titleText").getNamedComponent("text").text = "Waiting for players..."
		elif i>=20:
			findByName("titleText").getNamedComponent("text").text = "Waiting for players.."
		elif i>=0:
			findByName("titleText").getNamedComponent("text").text = "Waiting for players."
