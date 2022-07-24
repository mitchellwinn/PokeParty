import game
import asyncio
import random
from gameobject import GameObject, findByName
from sprite import Sprite
from text import Text
from audio import playSound, playMusic, stopMusic
import pygame as pg
from client import Client

async def join():
	global roomName
	roomName = ""
	inputDone = False
	stopMusic()
	await asyncio.sleep(.25)
	playMusic("NBtown.mp3")
	game.gameObjects.append(GameObject("titleText",[game.windowDimensions[0]/2,game.windowDimensions[1]/2.2]))
	findByName("titleText").addComponent(Text("Enter Room Name!","pokemon1.ttf"),"text")
	game.gameObjects.append(GameObject("titleText2",[game.windowDimensions[0]/2,game.windowDimensions[1]/1.8]))
	findByName("titleText2").addComponent(Text("","pokemon1.ttf"),"text")
	blinker = " "
	i=0
	user_text = ""
	while inputDone==False:
		for event in pg.event.get():
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_BACKQUOTE:
					stopMusic()
					playSound("SFX_PRESS_AB.wav")
					game.gameState = "title"
					game.gameObjects.clear()
					inputDone=True
					return
				elif event.key == pg.K_RETURN and len(user_text)>0:
					stopMusic()
					playSound("SFX_PRESS_AB.wav")
					inputDone=True
					game.gameObjects.clear()
					asyncio.create_task(connectRoom(user_text))
					game.gameState = "connectingToRoom"
					return
				elif event.key == pg.K_BACKSPACE:
					user_text = user_text[0:-1]
				elif event.key == pg.K_ESCAPE:
					game.programLive = False
				else:
					user_text += event.unicode
		findByName("titleText2").getNamedComponent("text").text = user_text+blinker
		if game.frame%60>=30:
			blinker = "l"
		elif game.frame%60>=0:
			blinker = " "
		await asyncio.sleep(0)

async def connectRoom(room):
	game.gameObjects.append(GameObject("titleText",[game.windowDimensions[0]/2,game.windowDimensions[1]*.5]))
	findByName("titleText").addComponent(Text("PLEASE  WAIT","pokemon1.ttf"),"text")
	if game.playerObject.getNamedComponent("client")==-1:
		game.playerObject.addComponent(Client(room),"client")
	else:
		game.playerObject.components.remove(game.playerObject.getNamedComponent("client"))
		game.playerObject.addComponent(Client(room),"client")
	while game.playerObject.getNamedComponent("client").connected == "UNDECIDCED":
		await asyncio.sleep(0)
	if game.playerObject.getNamedComponent("client").connected=="FAILURE":
		game.playerObject.removeComponent("client")
		findByName("titleText").getNamedComponent("text").text = "Failed to reach Server!"
		playSound("SFX_PRESS_AB.wav")
		await asyncio.sleep(.75)
		game.gameState = "title"
		game.gameObjects.clear()
		return
	if len(game.allPlayers)==1:
		findByName("titleText").getNamedComponent("text").text = f"Successfully CREATED {room}!{len(game.allPlayers)}/{4}"
	elif len(game.allPlayers)>1:
		findByName("titleText").getNamedComponent("text").text = f"Successfully JOINED {room}!{len(game.allPlayers)}/{4}"
	else:
		playSound("SFX_PRESS_AB.wav")
		await asyncio.sleep(.75)
		game.gameState = "title"
		game.gameObjects.clear()
		return
	playSound("SFX_PRESS_AB.wav")
	await asyncio.sleep(.75)
	game.gameState = "inRoom"
	asyncio.create_task(inRoom())


async def inRoom():
	global roomName,ready
	ready = False
	hasRoom = False
	while(hasRoom==False):
		try:
			roomName = game.playerObject.getNamedComponent("client").room
		except:
			await asyncio.sleep(0)
	inputDone = False
	await asyncio.sleep(.25)
	playMusic("052 National Park.mp3")
	game.gameObjects.append(GameObject("room",[game.windowDimensions[0]*.05,game.windowDimensions[1]*.1]))
	findByName("room").addComponent(Text(f"ROOM[{roomname}]","pokemon1.ttf",16,"left"),"text")
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
