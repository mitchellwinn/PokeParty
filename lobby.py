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

async def lobbyMain():
	game.gameObjects.clear()
	await join()
	
async def join():
	await asyncio.sleep(.25)
	global roomName
	roomName = ""
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
	
	while game.gameState=="lobby":
		game.typeInput = ""
		inputs = game.getPlayerInputsNow()
		if inputs[9] == True:
			stopMusic()
			playSound("SFX_PRESS_AB.wav")
			return
		elif inputs[12] == True and len(user_text)>0:
			stopMusic()
			playSound("SFX_PRESS_AB.wav")
			inputDone=True
			game.gameObjects.clear()
			await connectRoom(user_text)
			return
		elif inputs[13] == True:
			user_text = user_text[0:-1]
		elif game.typeInput != "":
			user_text += game.typeInput
		findByName("titleText2").getNamedComponent("text").text = user_text+blinker
		if game.frame%60>=30:
			blinker = ""
		elif game.frame%60>=0:
			blinker = "l"
		await asyncio.sleep(game.timestep)

async def connectRoom(room):
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
		await asyncio.sleep(.75)
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
		await asyncio.sleep(.75)
		#game.gameState = "title"
		game.gameObjects.clear()
		return
	findByName("titleText2").getNamedComponent("text").text = f"{room}!"
	findByName("titleText3").getNamedComponent("text").text = f"{len(game.allPlayers)+1} players so far."
	playSound("SFX_HEAL_AILMENT.wav")
	await asyncio.sleep(2.5)
	roomName = game.playerObject.getNamedComponent("client").room
	await inRoom()
	

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
	await roomSettings()

async def roomSettings():
	i=0
	print("roomSettings")
	while game.gameState=="inRoom":
		time1=time.time()
		inputs = game.getPlayerInputsNow()
		thisClient = game.playerObject.getNamedComponent("client")
		if thisClient.ready:
			ready = True
		else:
			ready = False
		if inputs[9]==True:#go back to title
			stopMusic()
			game.playerObject.getNamedComponent("client").send(SimpleData("!DISCONNECT",[game.playerObject.getNamedComponent("client").id]).getAsDataString(),False)
			game.playerObject.removeComponent("client")
			game.playerObject.removeComponent("sprite")
			playSound("SFX_PRESS_AB.wav")
			game.gameState = "title"
			game.gameObjects.clear()
			game.allPlayers.clear()
			return
		if inputs[14]==True:#ready or unready

			if thisClient.ready:
				findByName("ready"+str(thisClient.id)).getNamedComponent("sprite").fileChange("waiting.gif")
				thisClient.ready = False
				playSound("SFX_ENTER_PC.wav")
			else:
				findByName("ready"+str(thisClient.id)).getNamedComponent("sprite").fileChange("ready.gif")
				thisClient.ready = True
				playSound("SFX_DEX_PAGE_ADDED.wav")
			findByName("ready"+str(thisClient.id)).getNamedComponent("sprite").playing = True
		if inputs[1]==True and ready == False:
			thisClient.trainer+=1
			if(thisClient.trainer>game.TRAINERS):
				thisClient.trainer=1
			game.playerObject.getNamedComponent("sprite").fileChange(str(thisClient.trainer)+".png")
			game.playerObject.getNamedComponent("client").send(SimpleData("UPDATE",[thisClient.id,thisClient.trainer,thisClient.starter,thisClient.ready]).getAsDataString(),False)
		if inputs[2]==True and ready == False:
			thisClient.trainer+=-1
			if(thisClient.trainer<1):
				thisClient.trainer=game.TRAINERS
			game.playerObject.getNamedComponent("sprite").fileChange(str(thisClient.trainer)+".png")
			game.playerObject.getNamedComponent("client").send(SimpleData("UPDATE",[thisClient.id,thisClient.trainer,thisClient.starter,thisClient.ready]).getAsDataString(),False)
		if  inputs[3]==True and ready == False:
			thisClient.starter+=-1
			if(thisClient.starter<0):
				thisClient.starter=5
			thisClient.idstarter=game.starterList[thisClient.starter]
			findByName("pokemon"+str(thisClient.id)).getNamedComponent("sprite").fileChange(str(thisClient.idstarter)+".png")
			game.playerObject.getNamedComponent("client").send(SimpleData("UPDATE",[thisClient.id,thisClient.trainer,thisClient.starter,thisClient.ready]).getAsDataString(),False)
			print(thisClient.starter)
			print(thisClient.idstarter)
		if  inputs[4]==True and ready == False:
			thisClient.starter+=1
			if(thisClient.starter>5):
				thisClient.starter=0
			thisClient.idstarter=game.starterList[thisClient.starter]
			findByName("pokemon"+str(thisClient.id)).getNamedComponent("sprite").fileChange(str(thisClient.idstarter)+".png")
			game.playerObject.getNamedComponent("client").send(SimpleData("UPDATE",[thisClient.id,thisClient.trainer,thisClient.starter,thisClient.ready]).getAsDataString(),False)
			print(thisClient.starter)
			print(thisClient.idstarter)
		if ready==False:
			findByName("titleText2").getNamedComponent("text").text = "Press 'R' to READY"
		else:
			findByName("titleText2").getNamedComponent("text").text = "READY!"
		time2 = time.time()
		i+= (time2-time1)
		if i>60:
			i=0
		if i>=40:
			findByName("titleText").getNamedComponent("text").text = "Waiting for players..."
		elif i>=20:
			findByName("titleText").getNamedComponent("text").text = "Waiting for players.."
		elif i>=0:
			findByName("titleText").getNamedComponent("text").text = "Waiting for players."
		await asyncio.sleep(game.timestep)
	
