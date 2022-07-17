import pygame as pg
from PIL import Image, ImageSequence

class Sprite(object):


	def fileChange(self, file):
		self.file=file
		self.img = pg.image.load(self.filePath+self.file)


	def gifInit(self):
		self.waitFrames = 4
		self.framesWaited = 0
		self.frame = 1
		self.PILimg = Image.open(self.filePath+self.file)
		self.frames = []
		for i in ImageSequence.Iterator(self.PILimg):
			mode = i.mode
			size = i.size
			data = i.tobytes()
			toAppend = pg.image.fromstring(data,size,mode)
			self.frames.append(toAppend)
		self.playing = False

	def gifCheck(self):
		if self.playing==False:
			return
		self.framesWaited+=1
		if self.framesWaited>self.waitFrames:
			self.framesWaited=0
			self.frame+=1
			if self.frame>=len(self.frames):
				playing = False
				self.frame = len(self.frames)-1
		self.img = self.frames[self.frame]

	def __init__(self,*args):
		self.filePath = "sprites\\"+args[1]
		self.file=args[0]
		self.img = pg.image.load(self.filePath+self.file)
		if len(args)>2:
			self.fileType = args[2]
		else:
			self.fileType = "png"
		if(self.fileType=="gif"):
			self.gifInit()

