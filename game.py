import pygame as pg
import asyncio
import ctypes
import random
from sprite import Sprite
from gameobject import findByName, GameObject
from client import SimpleData
from audio import stopMusic

#all global variables to be used by game
def __init__():
	global gameObjects, timestep, playerInputs, programLive, windowDimensions, scale, volume, full, frame, border, playerObject, starterList, allPlayers, gameVolume, iconShow
	iconShow = 0
	myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
	ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
	timestep = 1/60
	gameObjects = []
	allPlayers = []
	starterList = [1,4,7,25,52,133]
	scale=2
	windowDimensions = [160,144]
	programLive = True
	volume = .1
	gameVolume = 1
	frame = 0
	full = False
	border = pg.image.load("sprites\\frame.png")
	border = pg.transform.scale(border, (border.get_rect().width*4, border.get_rect().height*4))
#update playrInput global variable to be used throughout program
def playerInputsGet():
	global typeInput, typing, inputsFalse, inputs, gameState
	typing = False
	if gameState=="lobby":
		typing = True
	inputsFalse = [False,False,False,False,False,False,False,False,False,False,False,False,False,False]
	if typing == False:
		typeInput = ""
		inputs = inputsFalse
	events = pg.event.get()
	for event in events:
		if event.type == pg.KEYDOWN:
			typeInput = event.unicode
			if event.key == pg.K_ESCAPE:
				print("Pressed ESC")
				inputs[0] = True
			elif event.key == pg.K_UP:
				inputs[1] = True
			elif event.key == pg.K_DOWN:
				inputs[2] = True
			elif event.key == pg.K_LEFT:
				inputs[3] = True
			elif event.key == pg.K_RIGHT:
				inputs[4] = True
			elif event.key == pg.K_RIGHTBRACKET:
				inputs[5] = True
			elif event.key == pg.K_LEFTBRACKET:
				inputs[6] = True
			elif event.key == pg.K_z:
				inputs[7] = True
			elif event.key == pg.K_F11:
				inputs[8] = True
			elif event.key == pg.K_BACKQUOTE:
				inputs[9] = True
			elif event.key == pg.K_PAGEUP:
				inputs[10] = True
			elif event.key == pg.K_PAGEDOWN:
				inputs[11] = True
			elif event.key == pg.K_RETURN:
				inputs[12] = True
			elif event.key == pg.K_BACKSPACE:
				inputs[13] = True
	return inputs

#main operations of pygame
async def gameMain():
	#gameMain is called once
	global gameObjects, timestep, playerInputs, programLive, windowDimensions, screen, scale, gameState, frame
	#pygame window is initialized with base dimensions
	pg.init()
	img = pg.image.load('sprites\\windowIcon.png')
	pg.display.set_icon(img)
	pg.display.set_caption('PokeParty')
	screen = pg.display.set_mode(size=(windowDimensions[0]*scale, windowDimensions[1]*scale), flags=0, depth=0, display=0, vsync=0)
	gameState = "title"
	#as long as we are still running the program it is live
	while programLive:
		playerInputs = playerInputsGet()
		if playerInputs[0]==True:
			programLive = False
		if playerInputs[5]==True:
			zoom(1)
		elif playerInputs[6]==True:
			zoom(-1)
		if playerInputs[10]==True:
			asyncio.create_task(volumeMod(1))
		elif playerInputs[11]==True:
			asyncio.create_task(volumeMod(-1))
		if playerInputs[8]==True:
			fullscreen()

		#game is computed at 60fps
		updateDisplay()
		await asyncio.sleep(timestep)
		frame+=1
	stopMusic()
	pg.display.quit()
	try:
		playerObject.getNamedComponent("client").send(SimpleData("!DISCONNECT",[playerObject.getNamedComponent("client").id]).getAsDataString(),False)
	except:
		print("Failed to send !DISCONNECT message")
	quit()

async def volumeMod(amount):
	global volume, gameVolume, iconShow
	iconShow+=1
	print(f"add 1 to iconShow to give: {iconShow}")
	gameVolume += amount
	if gameVolume<0:
		gameVolume = 0
	elif gameVolume>4:
		gameVolume = 4
	thisVolume = gameVolume
	try:
		findByName(f"volumeIcon").destroy()
	except:
		None
	instantiate(f"volumeIcon",[0,0])
	findByName(f"volumeIcon").addComponent(Sprite(f"volumeIcon{thisVolume}.png","","png","topleft"),f"sprite")
	pg.mixer.music.set_volume(volume*.7*thisVolume)
	await asyncio.sleep(1)
	print("just slept for 1 second")
	iconShow-=1
	print(f"subtract 1 from iconShow to give: {iconShow}")
	if(iconShow>0):
		return
	try:
		findByName(f"volumeIcon").destroy()
	except:
		None

def zoom(amount):
	global scale, screen, full, frame
	if(full):
		return
	scale += amount
	if scale<1:
		scale = 1
	elif scale>4:
		scale = 4
	else:
		screen = pg.display.set_mode(size=(windowDimensions[0]*scale, windowDimensions[1]*scale), flags=0, depth=0, display=0, vsync=0)
	frame = 0
	updateDisplay()

def fullscreen():
	global full, screen, scale, windowDimensions, frame
	if full:
		scale = 2
		screen = pg.display.set_mode(size=(windowDimensions[0]*scale, windowDimensions[1]*scale), flags=0, depth=0, display=0, vsync=0)
		full = False
		frame = 0
		updateDisplay()
		
	else:
		scale = 4
		screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
		full = True
		frame = 0
		updateDisplay()
		

def instantiate(name,position):
	gameObjects.append(GameObject(name,position))

def updateDisplay():
	global screen, scale, full,w ,h, frame, border
	w, h = screen.get_size()
	screen.fill([255,255,255])
	for gobj in (gameObjects+allPlayers):
		if gobj.getNamedComponent("sprite")!=-1:
			drawSprites(gobj.getNamedComponent("sprite"),gobj)
		if gobj.getNamedComponent("text")!=-1:
			drawText(gobj.getNamedComponent("text"),gobj)
	if playerObject.getNamedComponent("sprite")!=-1:
			drawSprites(playerObject.getNamedComponent("sprite"),playerObject)
	if full:
		screen.blit(border,border.get_rect(center=((w/2),(h/2))))	
	pg.display.update()

def drawSprites(sprite,gobj):
	global screen, full, scale, w, h, frame
	if frame % 5 == 0:	
		if sprite.fileType == "gif":
			sprite.gifCheck()
	img = pg.transform.scale(sprite.img, (sprite.img.get_rect().width*scale, sprite.img.get_rect().height*scale))
	if(sprite.anchor=="center"):	
		if full == False:
			screen.blit(img,img.get_rect(center=(round(gobj.transform.position[0])*scale,round(gobj.transform.position[1])*scale)))
		elif full == True:
			screen.blit(img,img.get_rect(center=(round(gobj.transform.position[0]-windowDimensions[0]/2)*scale+w/2,round(gobj.transform.position[1]-windowDimensions[1]/2)*scale+h/2)))
	elif(sprite.anchor=="topleft"):	
		if full == False:
			screen.blit(img,img.get_rect(topleft=(round(gobj.transform.position[0])*scale,round(gobj.transform.position[1])*scale)))
		elif full == True:
			screen.blit(img,img.get_rect(topleft=(round(gobj.transform.position[0]-windowDimensions[0]/2)*scale+w/2,round(gobj.transform.position[1]-windowDimensions[1]/2)*scale+h/2)))

def drawText(text,gobj):
	global screen, w, h, full, scale, frame
	#print("attempting to render "+text.text+" in "+text.file)
	if frame % 5 == 0:	
		text.font = pg.font.Font(text.filePath+text.file,round(text.size*(scale/2)))
		text.img = text.font.render(text.text, True, (0,0,0), (255,255,255))
		text.rect = text.img.get_rect()
	try:
		if(text.anchor == "center"):
			text.rect.center = [round(gobj.transform.position[0])*scale,round(gobj.transform.position[1])*scale]
		elif(text.anchor == "left"):
			text.rect.midleft = [round(gobj.transform.position[0])*scale,round(gobj.transform.position[1])*scale]
		elif(text.anchor == "right"):
			text.rect.midright = [round(gobj.transform.position[0])*scale,round(gobj.transform.position[1])*scale]
	except:
		print("")
	if full == False:
		screen.blit(text.img,text.rect)
	elif full == True:
		try:
			if(text.anchor == "center"):
				text.rect.center = [round(gobj.transform.position[0]-windowDimensions[0]/2)*scale+w/2,round(gobj.transform.position[1]-windowDimensions[1]/2)*scale+h/2]
			elif(text.anchor == "left"):
				text.rect.midleft = [round(gobj.transform.position[0]-windowDimensions[0]/2)*scale+w/2,round(gobj.transform.position[1]-windowDimensions[1]/2)*scale+h/2]
			elif(text.anchor == "right"):
				text.rect.midright = [round(gobj.transform.position[0]-windowDimensions[0]/2)*scale+w/2,round(gobj.transform.position[1]-windowDimensions[1]/2)*scale+h/2]
			screen.blit(text.img,text.rect)
		except:
			print("")

#---USEFUL MODULE FUNCTIONS FOR ALL GAMES---------------------------------------------------------------------

#adds numbers of 2 lists at each index
def addNumbers(l1,l2):
	k=0
	l3 = []
	for i in l1:
		l3.append(l2[k]+i)
		k=k+1
	return l3

#subtracts numbers of 2 lists at each index
def subNumbers(l1,l2):
	k=0
	l3 = []
	for i in l1:
		l3.append(i-l2[k])
		k=k+1
	return l3

#multiplies numbers of 2 lists at each index
def multNumbers(l1,l2):
	k=0
	l3 = []
	for i in l1:
		l3.append(l2[k]*i)
		k=k+1
	return l3

#scales numbers in a list by some value
def scaleList(list,scale):
	newList = []
	for i in list:
		p=i*scale
		newList.append(p)
	return newList
