import game
import asyncio
import random
from gameobject import GameObject, findByName
from sprite import Sprite
from text import Text
from audio import playSound, playMusic, stopMusic
from lobby import lobbyStart
from threading import Thread

async def titleGo():
	#print("Triggered titleGo from game.py")
	await asyncio.sleep(.75)
	playSound("SFX_TINK.wav")
	game.gameObjects.append(GameObject("titleText",[game.windowDimensions[0]/2.6,game.windowDimensions[1]/2.2]))
	findByName("titleText").addComponent(Text("By Mitchell Winn","pokemon1.ttf"),"text")
	game.gameObjects.append(GameObject("titleText2",[game.windowDimensions[0]/1.3,game.windowDimensions[1]/1.8]))
	findByName("titleText2").addComponent(Text("2022","pokemon1.ttf"),"text")
	await asyncio.sleep(1.5)
	findByName("titleText").destroy()
	findByName("titleText2").destroy()
	await asyncio.sleep(.25)
	#playSound("SFX_INTRO_CRASH.wav")
	game.gameObjects.append(GameObject("titlePokemon",[game.windowDimensions[0]*-.25,game.windowDimensions[1]*.775]))
	game.gameObjects.append(GameObject("titleTrainer",[game.windowDimensions[0]*.165,game.windowDimensions[1]*.775]))
	findByName("titleTrainer").addComponent(Sprite(str(random.randint(1,game.TRAINERS))+".png","trainers\\"),"sprite")
	asyncio.create_task(cyclePokemon())
	game.gameObjects.append(GameObject("title",[game.windowDimensions[0]/2,0]))
	findByName("title").addComponent(Sprite("title1black.png","title\\"),"sprite")
	await(findByName("title").transform.moveOverTime([game.windowDimensions[0]/2,game.windowDimensions[1]/3],.45))
	findByName("title").getNamedComponent("sprite").fileChange("title1.png")
	playSound("SFX_INTRO_CRASH.wav")
	await asyncio.sleep(.25)

async def titleMenu():
	game.gameObjects.append(GameObject("menu1",[game.windowDimensions[0]*.85,game.windowDimensions[1]*.715]))
	game.gameObjects.append(GameObject("menu2",[game.windowDimensions[0]*.85,game.windowDimensions[1]*.79]))
	game.gameObjects.append(GameObject("pointer",[game.windowDimensions[0]*.725,game.windowDimensions[1]*.715]))
	findByName("pointer").addComponent(Sprite("pointer.png",""),"sprite")
	findByName("menu1").addComponent(Text("PLAY","pokemon1.ttf"),"text")
	findByName("menu2").addComponent(Text("EXIT","pokemon1.ttf"),"text")
	await asyncio.sleep(.25)
	playMusic("08 Cerulean City's Theme.mp3")
	choice = 0
	while game.gameState == "title":
		if(game.playerInputs[1]==True):
			choice-=1
		elif(game.playerInputs[2]==True):
			choice+=1
		if choice>1:
			choice = 1
		if choice<0:
			choice = 0
		if game.playerInputs[7]==True:
			playSound("SFX_PRESS_AB.wav")
			game.gameObjects.clear()
			if choice==0:
				game.gameState = "lobby"
				thread = Thread(target=lobbyStart)
				thread.start()
				while thread.is_alive():
					await asyncio.sleep(0)
				game.gameState = "title"
				return
			if choice==1:
				await asyncio.sleep(.25)
				game.programLive = False
				return
		findByName("pointer").transform.position = [game.windowDimensions[0]*.725,game.windowDimensions[1]*(.715+(choice*.075))]
		await asyncio.sleep(0)
	findByName("menu1").destroy()
	findByName("menu2").destroy()

async def cyclePokemon():
	findByName("titlePokemon").addComponent(Sprite(str(random.randint(1,251))+".gif","pokemon\\","gif"),"sprite")
	while game.gameState == "title":
		
		asyncio.create_task(findByName("titlePokemon").transform.smoothMoveOverTime([game.windowDimensions[0]*.45,game.windowDimensions[1]*.775],.45))
		await(findByName("titleTrainer").transform.smoothMoveOverTime([game.windowDimensions[0]*.165,game.windowDimensions[1]*.775],.45))
		await asyncio.sleep(.3)
		if(game.gameState != "title"):
			return
		findByName("titlePokemon").getNamedComponent("sprite").playing = True
		await asyncio.sleep(2)
		if(game.gameState != "title"):
			return
		
		asyncio.create_task(findByName("titlePokemon").transform.smoothMoveOverTime([game.windowDimensions[0]*-.25,game.windowDimensions[1]*.775],.9))
		await(findByName("titleTrainer").transform.smoothMoveOverTime([game.windowDimensions[0]*-.25,game.windowDimensions[1]*.775],1.1))
		try:
			findByName("titlePokemon").transform.position=[game.windowDimensions[0]*-.25,game.windowDimensions[1]*.775]
		except:
			return
		findByName("titleTrainer").getNamedComponent("sprite").fileChange(str(random.randint(1,game.TRAINERS))+".png")
		findByName("titlePokemon").getNamedComponent("sprite").fileChange(str(random.randint(1,251))+".gif")
		#findByName("titlePokemon").getNamedComponent("sprite").gifInit()
	findByName("title").destroy()
	findByName("titlePokemon").destroy()
	findByName("titleTrainer").destroy()
