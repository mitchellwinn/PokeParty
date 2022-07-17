import game
import asyncio
import random
from gameobject import GameObject, findByName
from sprite import Sprite
from text import Text
from audio import playSound, playMusic

async def titleGo():
	print("Triggered titleGo from game.py")
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
	playSound("SFX_INTRO_CRASH.wav")
	game.gameObjects.append(GameObject("titlePokemon",[game.windowDimensions[0]*-.25,game.windowDimensions[1]*.775]))
	game.gameObjects.append(GameObject("titleTrainer",[game.windowDimensions[0]*.165,game.windowDimensions[1]*.775]))
	findByName("titleTrainer").addComponent(Sprite(str(random.randint(1,15))+".png","trainers\\"),"sprite")
	asyncio.create_task(cyclePokemon())
	game.gameObjects.append(GameObject("title",[game.windowDimensions[0]/2,0]))
	findByName("title").addComponent(Sprite("title1black.png","title\\"),"sprite")
	await(findByName("title").transform.moveOverTime([game.windowDimensions[0]/2,game.windowDimensions[1]/3],.45))
	findByName("title").getNamedComponent("sprite").file = "title1.png"

async def titleMenu():
	game.gameObjects.append(GameObject("menu1",[game.windowDimensions[0]*.765,game.windowDimensions[1]*.715]))
	game.gameObjects.append(GameObject("menu2",[game.windowDimensions[0]*.765,game.windowDimensions[1]*.79]))
	findByName("menu1").addComponent(Text("HOST","pokemon1.ttf"),"text")
	findByName("menu2").addComponent(Text("JOIN","pokemon1.ttf"),"text")
	await asyncio.sleep(.25)
	playMusic("08 Cerulean City's Theme.mp3")
	while game.gameState == "title":
		await asyncio.sleep(0)
	findByName("menu1").destroy()
	findByName("menu2").destroy()

async def cyclePokemon():
	findByName("titlePokemon").addComponent(Sprite(str(random.randint(1,151))+".gif","pokemon\\","gif"),"sprite")
	while game.gameState == "title":
		await(findByName("titlePokemon").transform.smoothMoveOverTime([game.windowDimensions[0]*.4,game.windowDimensions[1]*.775],.45))
		findByName("titlePokemon").getNamedComponent("sprite").playing = True
		await asyncio.sleep(2)
		await(findByName("titlePokemon").transform.smoothMoveOverTime([game.windowDimensions[0]*-.25,game.windowDimensions[1]*.775],.9))
		findByName("titlePokemon").transform.position=[game.windowDimensions[0]*-.25,game.windowDimensions[1]*.775]
		findByName("titlePokemon").getNamedComponent("sprite").fileChange(str(random.randint(1,151))+".gif")
		findByName("titlePokemon").getNamedComponent("sprite").gifInit()
	findByName("title").destroy()
	findByName("titlePokemon").destroy()
	findByName("titleTrainer").destroy()
