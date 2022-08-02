import pygame as pg
import game
from PIL import Image, ImageSequence

class Sprite(object):

	def gifInit(self):
		self.frame = 0
		self.PILimg = Image.open(self.filePath+self.file)
		self.frames = []
		for i in range(self.PILimg.n_frames):
			self.PILimg.seek(i)
			rgba = self.PILimg.convert("RGBA")
			toAppend = pg.image.fromstring(rgba.tobytes(),rgba.size,rgba.mode)
			#print(toAppend)
			self.frames.append(toAppend)
		self.playing = False
		self.img = self.frames[self.frame]

	def fileChange(self, file):
		self.file=file
		self.frame = 0
		if file.count(".gif")==	0:
			self.fileType = "png"
			self.img = pg.image.load(self.filePath+self.file)
		else: 
			self.fileType="gif"
			self.gifInit()

	def gifCheck(self):
		if self.playing==False:
			return
		self.frame+=1
		if self.frame>=len(self.frames):
			if self.looping == False:
					self.playing = False
					self.frame = len(self.frames)-1
			else:
				self.frame = 0
		self.img = self.frames[self.frame]

	def __init__(self,*args):
		self.looping = False
		self.anchor = "center"
		self.filePath = "sprites\\"+args[1]
		#self.img = pg.image.load(self.filePath+self.file)
		if len(args)>2:
			self.fileType = args[2]
		else:
			self.fileType = "png"
		self.fileChange(args[0])
		if(len(args)>3):
			self.anchor=args[3]

