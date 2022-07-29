import game
import time
import random
from gameobject import GameObject, findByName
from sprite import Sprite
from text import Text
from audio import playSound, playMusic, stopMusic
import pygame as pg
from client import Client, SimpleData

def lobbyStart():
	join()
	game.gameObjects.clear()

def join():
	time.sleep(.25)
	global roomName
	roomName = ""
	inputDone = False
	stopMusic()
	playMusic("NBtown.mp3")
	game.gameObjects.append(GameObject("titleText",[game.windowDimensions[0]/2,game.windowDimensions[1]/2.2]))
	findByName("titleText").addComponent(Text("Enter Room Name!","pokemon1.ttf"),"text")
	game.gameObjects.append(GameObject("titleText2",[game.windowDimensions[0]/2,game.windowDimensions[1]/1.8]))
	findByName("titleText2").addComponent(Text("","pokemon1.ttf"),"text")
	game.frame = 0
	game.updateDisplay()
	blinker = " "
	i=0
	user_text = ""
	game.typeInput = ""
	while inputDone==False:
		if game.playerInputs[9] == True:
			stopMusic()
			playSound("SFX_PRESS_AB.wav")
			game.gameObjects.clear()
			return
		elif game.playerInputs[0] == True:
			game.programLive = False
			return
		elif game.playerInputs[12] == True and len(user_text)>0:
			stopMusic()
			playSound("SFX_PRESS_AB.wav")
			inputDone=True
			game.gameObjects.clear()
			connectRoom(user_text)
			game.gameState = "connectingToRoom"
			return
		elif game.playerInputs[13] == True:
			user_text = user_text[0:-1]
		else:
			user_text += game.typeInput
		findByName("titleText2").getNamedComponent("text").text = user_text+blinker
		if game.frame%60>=30:
			blinker = ""
		elif game.frame%60>=0:
			blinker = "l"
		game.inputs = game.inputsFalse
		game.typeInput = ""
		time.sleep(game.timestep)

def connectRoom(room):
	global roomName
	game.gameObjects.append(GameObject("titleText",[game.windowDimensions[0]/2,game.windowDimensions[1]*.5]))
	findByName("titleText").addComponent(Text("PLEASE  WAIT","pokemon1.ttf"),"text")
	if game.playerObject.getNamedComponent("client")==-1:
		game.playerObject.addComponent(Client(room),"client")
	else:
		game.playerObject.removeComponent("client")
		game.playerObject.addComponent(Client(room),"client")
	game.playerObject.getNamedComponent("client").connect()
	if game.playerObject.getNamedComponent("client").connected=="FAILURE":
		game.playerObject.removeComponent("client")
		findByName("titleText").getNamedComponent("text").text = "Failed to reach Server!"
		playSound("SFX_PRESS_AB.wav")
		time.sleep(.75)
		game.gameObjects.clear()
		return
	game.gameObjects.clear()
	game.gameObjects.append(GameObject("titleText",[game.windowDimensions[0]/2,game.windowDimensions[1]*.36]))
	findByName("titleText").addComponent(Text("","pokemon1.ttf"),"text")
	game.gameObjects.append(GameObject("titleText2",[game.windowDimensions[0]/2,game.windowDimensions[1]*.5]))
	findByName("titleText2").addComponent(Text("","pokemon1.ttf"),"text")
	game.gameObjects.append(GameObject("titleText3",[game.windowDimensions[0]/2,game.windowDimensions[1]*.74]))
	findByName("titleText3").addComponent(Text("","pokemon1.ttf"),"text")
	if len(game.allPlayers+1)==1:
		findByName("titleText").getNamedComponent("text").text = f"Successfully CREATED"
	elif len(game.allPlayers+1)>1:
		findByName("titleText").getNamedComponent("text").text = f"Successfully JOINED"
	else:
		findByName("titleText").getNamedComponent("text").text = f"Error initializing room!"
		playSound("SFX_PRESS_AB.wav")
		time.sleep(.75)
		#game.gameState = "title"
		game.gameObjects.clear()
		return
	findByName("titleText2").getNamedComponent("text").text = f"{room}!"
	findByName("titleText3").getNamedComponent("text").text = f"{len(game.allPlayers)} players so far."
	playSound("SFX_HEAL_AILMENT.wav")
	time.sleep(2.5)
	game.gameState = "inRoom"
	roomName = game.playerObject.getNamedComponent("client").room
	inRoom()

def inRoom():
	global roomName,ready
	game.gameObjects.clear()
	ready = False
	inputDone = False
	time.sleep(.25)
	playMusic("052 National Park.mp3")
	game.gameObjects.append(GameObject("room",[game.windowDimensions[0]*.05,game.windowDimensions[1]*.1]))
	findByName("room").addComponent(Text(f"ROOM[{roomName}]","pokemon1.ttf",16,"left"),"text")
	game.gameObjects.append(GameObject("titleText",[game.windowDimensions[0]*.175,game.windowDimensions[1]*.35]))
	findByName("titleText").addComponent(Text("Waiting for players","pokemon1.ttf",16,"left"),"text")
	game.gameObjects.append(GameObject("titleText2",[game.windowDimensions[0]/2,game.windowDimensions[1]*.5]))
	findByName("titleText2").addComponent(Text("Press 'R' to READY","pokemon1.ttf"),"text")
	game.gameObjects.append(GameObject("titleText3",[game.windowDimensions[0]/2,game.windowDimensions[1]*.65]))
	findByName("titleText3").addComponent(Text("Not all players are READY","pokemon1.ttf"),"text")
	i=0
	while inputDone==False:
		if game.playerInputs[9]==True:
			stopMusic()
			game.playerObject.getNamedComponent("client").send(SimpleData("!DISCONNECT",[playerObject.getNamedComponent("client").id]).getAsDataString(),False)
			playSound("SFX_PRESS_AB.wav")
			game.gameState = "title"
			game.gameObjects.clear()
			inputDone = True
			return
		if ready==False:
			findByName("titleText2").getNamedComponent("text").text = "Press 'R' to READY"
		else:
			findByName("titleText2").getNamedComponent("text").text = "READY!"
		time.sleep(game.timestep)
		i+=1
		if i>60:
			i=0
		if i>=40:
			findByName("titleText").getNamedComponent("text").text = "Waiting for players..."
		elif i>=20:
			findByName("titleText").getNamedComponent("text").text = "Waiting for players.."
		elif i>=0:
			findByName("titleText").getNamedComponent("text").text = "Waiting for players."
