import game
import time
import random
import asyncio
from threading import Thread
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
			#game.inputs = game.inputsFalse
			stopMusic()
			playSound("SFX_PRESS_AB.wav")
			game.gameObjects.clear()
			return
		elif game.playerInputs[0] == True:
			#game.inputs = game.inputsFalse
			game.programLive = False
			return
		elif game.playerInputs[12] == True and len(user_text)>0:
			#game.inputs = game.inputsFalse
			stopMusic()
			playSound("SFX_PRESS_AB.wav")
			inputDone=True
			game.gameObjects.clear()
			connectRoom(user_text)
			game.gameState = "connectingToRoom"
			return
		elif game.playerInputs[13] == True:
			#game.inputs = game.inputsFalse
			user_text = user_text[0:-1]
		elif game.typeInput != "":
			user_text += game.typeInput
			game.typeInput=""
		findByName("titleText2").getNamedComponent("text").text = user_text+blinker
		if game.frame%60>=30:
			blinker = ""
		elif game.frame%60>=0:
			blinker = "l"
		#game.inputs = game.inputsFalse
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
	game.playerObject.getNamedComponent("client").trainer = random.randint(1,game.TRAINERS)
	game.playerObject.getNamedComponent("client").starter = random.randint(0,5)
	game.playerObject.getNamedComponent("client").idstarter = game.starterList[game.playerObject.getNamedComponent("client").starter]
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
	if len(game.allPlayers)==0:
		findByName("titleText").getNamedComponent("text").text = f"Successfully CREATED"
	elif len(game.allPlayers)>0:
		findByName("titleText").getNamedComponent("text").text = f"Successfully JOINED"
	else:
		findByName("titleText").getNamedComponent("text").text = f"Error initializing room!"
		playSound("SFX_PRESS_AB.wav")
		time.sleep(.75)
		#game.gameState = "title"
		game.gameObjects.clear()
		return
	findByName("titleText2").getNamedComponent("text").text = f"{room}!"
	findByName("titleText3").getNamedComponent("text").text = f"{len(game.allPlayers)+1} players so far."
	playSound("SFX_HEAL_AILMENT.wav")
	time.sleep(2.5)
	roomName = game.playerObject.getNamedComponent("client").room
	asyncio.run(inRoom())

async def inRoom():
	global roomName, ready
	game.gameObjects.clear()
	ready = False
	inputDone = False
	time.sleep(.25)
	game.gameState = "inRoom"
	playMusic("052 National Park.mp3")
	game.gameObjects.append(GameObject("room",[game.windowDimensions[0]*.05,game.windowDimensions[1]*.1]))
	findByName("room").addComponent(Text(f"ROOM[{roomName}]","pokemon1.ttf",16,"left"),"text")
	game.gameObjects.append(GameObject("titleText",[game.windowDimensions[0]*.175,game.windowDimensions[1]*.175]))
	findByName("titleText").addComponent(Text("Waiting for players","pokemon1.ttf",16,"left"),"text")
	game.gameObjects.append(GameObject("titleText2",[game.windowDimensions[0]/2,game.windowDimensions[1]*.25]))
	findByName("titleText2").addComponent(Text("Press 'R' to READY","pokemon1.ttf"),"text")
	game.gameObjects.append(GameObject("titleText3",[game.windowDimensions[0]/2,game.windowDimensions[1]*.325]))
	findByName("titleText3").addComponent(Text("Not all players are READY","pokemon1.ttf"),"text")
	game.playerObject.transform.position = [game.windowDimensions[0]*.165,game.windowDimensions[1]*0.765]
	game.playerObject.addComponent(Sprite(str(game.playerObject.getNamedComponent("client").trainer)+".png","trainers\\","png"),"sprite")
	game.gameObjects.append(GameObject("label"+str(game.playerObject.getNamedComponent("client").id),[game.windowDimensions[0]*.165,game.windowDimensions[1]*.5]))
	findByName("label"+str(game.playerObject.getNamedComponent("client").id)).addComponent(Text(str(game.playerObject.getNamedComponent("client").name),"pokemon1.ttf"),"text")
	game.gameObjects.append(GameObject("pokemon"+str(game.playerObject.getNamedComponent("client").id),[game.windowDimensions[0]*.255,game.windowDimensions[1]*0.855]))
	findByName("pokemon"+str(game.playerObject.getNamedComponent("client").id)).addComponent(Sprite(str(game.playerObject.getNamedComponent("client").idstarter)+".png","pokemon\\","png"),"sprite")
	game.gameObjects.append(GameObject("ready"+str(game.playerObject.getNamedComponent("client").id),[game.windowDimensions[0]*.21,game.windowDimensions[1]*0.8955]))
	findByName("ready"+str(game.playerObject.getNamedComponent("client").id)).addComponent(Sprite("waiting.gif","","gif"),"sprite")
	findByName("ready"+str(game.playerObject.getNamedComponent("client").id)).getNamedComponent("sprite").looping=True
	findByName("ready"+str(game.playerObject.getNamedComponent("client").id)).getNamedComponent("sprite").playing=True
	i=0
	while inputDone==False:
		if game.playerObject.getNamedComponent("client").ready:
			ready = True
		else:
			ready = False
		if game.playerInputs[9]==True:
			await asyncio.sleep(.1)
			stopMusic()
			game.playerObject.getNamedComponent("client").send(SimpleData("!DISCONNECT",[game.playerObject.getNamedComponent("client").id]).getAsDataString(),False)
			game.playerObject.removeComponent("client")
			game.playerObject.removeComponent("sprite")
			playSound("SFX_PRESS_AB.wav")
			game.gameState = "title"
			game.gameObjects.clear()
			game.allPlayers.clear()
			inputDone = True
			return
		elif game.playerInputs[14]==True:
			await asyncio.sleep(.035)
			thisClient = game.playerObject.getNamedComponent("client")
			if thisClient.ready:
				findByName("ready"+str(thisClient.id)).getNamedComponent("sprite").fileChange("waiting.gif")
				thisClient.ready = False
			else:
				findByName("ready"+str(thisClient.id)).getNamedComponent("sprite").fileChange("ready.gif")
				thisClient.ready = True
			findByName("ready"+str(thisClient.id)).getNamedComponent("sprite").playing = True
			
			game.playerObject.getNamedComponent("client").send(SimpleData("UPDATE",[thisClient.id,thisClient.trainer,thisClient.starter,thisClient.ready]).getAsDataString(),False)
			#playSound("SFX_PRESS_AB.wav")
		elif game.playerInputs[1]==True and ready == False:
			await asyncio.sleep(.035)
			thisClient = game.playerObject.getNamedComponent("client")
			thisClient.trainer+=1
			if(thisClient.trainer>game.TRAINERS):
				thisClient.trainer=1
			game.playerObject.getNamedComponent("sprite").fileChange(str(thisClient.trainer)+".png")
			game.playerObject.getNamedComponent("client").send(SimpleData("UPDATE",[thisClient.id,thisClient.trainer,thisClient.starter,thisClient.ready]).getAsDataString(),False)
			#playSound("SFX_PRESS_AB.wav")
		elif game.playerInputs[2]==True and ready == False:
			await asyncio.sleep(.035)
			thisClient = game.playerObject.getNamedComponent("client")
			thisClient.trainer+=-1
			if(thisClient.trainer<1):
				thisClient.trainer=game.TRAINERS
			game.playerObject.getNamedComponent("sprite").fileChange(str(thisClient.trainer)+".png")
			game.playerObject.getNamedComponent("client").send(SimpleData("UPDATE",[thisClient.id,thisClient.trainer,thisClient.starter,thisClient.ready]).getAsDataString(),False)
			#playSound("SFX_PRESS_AB.wav")
		elif game.playerInputs[3]==True and ready == False:
			await asyncio.sleep(.035)
			thisClient = game.playerObject.getNamedComponent("client")
			thisClient.starter+=-1
			if(thisClient.starter<0):
				thisClient.starter=5
			thisClient.idstarter=game.starterList[thisClient.starter]
			findByName("pokemon"+str(thisClient.id)).getNamedComponent("sprite").fileChange(str(thisClient.idstarter)+".png")
			game.playerObject.getNamedComponent("client").send(SimpleData("UPDATE",[thisClient.id,thisClient.trainer,thisClient.starter,thisClient.ready]).getAsDataString(),False)
			#playSound("SFX_PRESS_AB.wav")
		elif game.playerInputs[4]==True and ready == False:
			await asyncio.sleep(.035)
			thisClient = game.playerObject.getNamedComponent("client")
			thisClient.starter+=1
			if(thisClient.starter>5):
				thisClient.starter=0
			thisClient.idstarter=game.starterList[thisClient.starter]
			findByName("pokemon"+str(thisClient.id)).getNamedComponent("sprite").fileChange(str(thisClient.idstarter)+".png")
			game.playerObject.getNamedComponent("client").send(SimpleData("UPDATE",[thisClient.id,thisClient.trainer,thisClient.starter,thisClient.ready]).getAsDataString(),False)
			#playSound("SFX_PRESS_AB.wav")
		if ready==False:
			findByName("titleText2").getNamedComponent("text").text = "Press 'R' to READY"
		else:
			findByName("titleText2").getNamedComponent("text").text = "READY!"
		
		i+=1
		if i>60:
			i=0
		if i>=40:
			findByName("titleText").getNamedComponent("text").text = "Waiting for players..."
		elif i>=20:
			findByName("titleText").getNamedComponent("text").text = "Waiting for players.."
		elif i>=0:
			findByName("titleText").getNamedComponent("text").text = "Waiting for players."
		await asyncio.sleep(game.timestep)
