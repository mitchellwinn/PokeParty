import pygame as pg
import asyncio
import ctypes
import random
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

#all global variables to be used by game
#                            
def __init__():
	global gameObjects, timestep, playerInputs, programLive, windowDimensions, scale, volume
	timestep = 1/60
	gameObjects = []
	scale=2
	windowDimensions = [160,144]
	programLive = True
	volume = .1

#update playrInput global variable to be used throughout program
def playerInputsGet():
	global gameObjects, timestep, playerInputs, programLive, windowDimensions
	#	       	    esc  ,up   ,down ,left ,right
	inputsFalse = [False,False,False,False,False,False,False]
	inputs = inputsFalse
	events = pg.event.get()
	for event in events:
		if event.type == pg.KEYDOWN:
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
	try:
		inputs	
		return inputs
	except:
		#print("no inputs to return")
		return inputsFalse

#main operations of pygame
async def gameMain():
	#gameMain is called once
	global gameObjects, timestep, playerInputs, programLive, windowDimensions, screen, scale, gameState
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

		#game is computed at 60fps
		updateDisplay()
		await asyncio.sleep(timestep)
	pg.display.quit()
	quit()

def zoom(amount):
	global scale, screen
	scale += amount
	if scale<1:
		scale = 1
	elif scale>4:
		scale = 4
	screen = pg.display.set_mode(size=(windowDimensions[0]*scale, windowDimensions[1]*scale), flags=0, depth=0, display=0, vsync=0)

def instantiate(name,position):
	gameObjects.append(GameObject(name,position))

def updateDisplay():
	global screen
	screen.fill([255,255,255])
	for gobj in gameObjects:
		if gobj.getNamedComponent("sprite")!=-1:
			drawSprites(gobj.getNamedComponent("sprite"),gobj)
		if gobj.getNamedComponent("text")!=-1:
			drawText(gobj.getNamedComponent("text"),gobj)
	pg.display.update()

def drawSprites(sprite,gobj):
	global screen
	sprite.img = pg.image.load(sprite.filePath+sprite.file)
	img = pg.transform.scale(sprite.img, (sprite.img.get_rect().width*scale, sprite.img.get_rect().height*scale))
	screen.blit(img,img.get_rect(center=(round(gobj.transform.position[0])*scale,round(gobj.transform.position[1])*scale)))

def drawText(text,gobj):
	global screen
	print("attempting to render "+text.text+" in "+text.file)
	font = pg.font.Font(text.filePath+text.file,round(16*(scale/2)))
	img = font.render(text.text, True, (0,0,0), (255,255,255))
	rect = img.get_rect()
	rect.center = gobj.transform.position[0]*scale,gobj.transform.position[1]*scale
	screen.blit(img,rect)
	

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
