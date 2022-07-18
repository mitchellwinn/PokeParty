import pygame as pg
import asyncio
import ctypes
import random
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

#all global variables to be used by game
def __init__():
	global gameObjects, timestep, playerInputs, programLive, windowDimensions, scale, volume, full
	timestep = 1/60
	gameObjects = []
	scale=2
	windowDimensions = [160,144]
	programLive = True
	volume = .1
	full = False

#update playrInput global variable to be used throughout program
def playerInputsGet():
	global gameObjects, timestep, playerInputs, programLive, windowDimensions
	inputsFalse = [False,False,False,False,False,False,False,False,False,False]
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
			elif event.key == pg.K_z:
				inputs[7] = True
			elif event.key == pg.K_F11:
				inputs[8] = True
			elif event.key == pg.K_x:
				inputs[9] = True
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
		if playerInputs[8]==True:
			fullscreen()

		#game is computed at 60fps
		updateDisplay()
		await asyncio.sleep(timestep)
	pg.display.quit()
	quit()

def zoom(amount):
	global scale, screen, full
	if(full):
		return
	scale += amount
	if scale<1:
		scale = 1
	elif scale>4:
		scale = 4
	else:
		screen = pg.display.set_mode(size=(windowDimensions[0]*scale, windowDimensions[1]*scale), flags=0, depth=0, display=0, vsync=0)

def fullscreen():
	global full, screen, scale, windowDimensions
	if full:
		scale = 2
		screen = pg.display.set_mode(size=(windowDimensions[0]*scale, windowDimensions[1]*scale), flags=0, depth=0, display=0, vsync=0)
		full = False
		
	else:
		scale = 4
		screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
		full = True
		

def instantiate(name,position):
	gameObjects.append(GameObject(name,position))

def updateDisplay():
	global screen, scale, full,w ,h
	w, h = screen.get_size()
	screen.fill([255,255,255])
	for gobj in gameObjects:
		if gobj.getNamedComponent("sprite")!=-1:
			drawSprites(gobj.getNamedComponent("sprite"),gobj)
		if gobj.getNamedComponent("text")!=-1:
			drawText(gobj.getNamedComponent("text"),gobj)
	if full:
		border = pg.image.load("sprites\\frame.png")
		border = pg.transform.scale(border, (border.get_rect().width*scale, border.get_rect().height*scale))
		screen.blit(border,border.get_rect(center=((w/2),(h/2))))	
	pg.display.update()

def drawSprites(sprite,gobj):
	global screen, full, scale, w, h
	if sprite.fileType == "png":
		sprite.img = pg.image.load(sprite.filePath+sprite.file)
	elif sprite.fileType =="gif":
		sprite.gifCheck()
	img = pg.transform.scale(sprite.img, (sprite.img.get_rect().width*scale, sprite.img.get_rect().height*scale))
	if full == False:
		screen.blit(img,img.get_rect(center=(round(gobj.transform.position[0])*scale,round(gobj.transform.position[1])*scale)))
	elif full == True:
		screen.blit(img,img.get_rect(center=(round(gobj.transform.position[0]-windowDimensions[0]/2)*scale+w/2,round(gobj.transform.position[1]-windowDimensions[1]/2)*scale+h/2)))

def drawText(text,gobj):
	global screen, w, h, full, scale
	#print("attempting to render "+text.text+" in "+text.file)
	font = pg.font.Font(text.filePath+text.file,round(text.size*(scale/2)))
	img = font.render(text.text, True, (0,0,0), (255,255,255))
	rect = img.get_rect()
	if(text.anchor == "center"):
		rect.center = [round(gobj.transform.position[0])*scale,round(gobj.transform.position[1])*scale]
	elif(text.anchor == "left"):
		rect.midleft = [round(gobj.transform.position[0])*scale,round(gobj.transform.position[1])*scale]
	elif(text.anchor == "right"):
		rect.midright = [round(gobj.transform.position[0])*scale,round(gobj.transform.position[1])*scale]
	if full == False:
		screen.blit(img,rect)
	elif full == True:
		if(text.anchor == "center"):
			rect.center = [round(gobj.transform.position[0]-windowDimensions[0]/2)*scale+w/2,round(gobj.transform.position[1]-windowDimensions[1]/2)*scale+h/2]
		elif(text.anchor == "left"):
			rect.midleft = [round(gobj.transform.position[0]-windowDimensions[0]/2)*scale+w/2,round(gobj.transform.position[1]-windowDimensions[1]/2)*scale+h/2]
		elif(text.anchor == "right"):
			rect.midright = [round(gobj.transform.position[0]-windowDimensions[0]/2)*scale+w/2,round(gobj.transform.position[1]-windowDimensions[1]/2)*scale+h/2]
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
