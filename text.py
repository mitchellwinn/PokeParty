import game
import pygame as pg
import asyncio

class Text(object):

	def __init__(self,*args):
		self.filePath = "fonts\\"
		self.file=args[1]
		self.text=args[0]
		if len(args)>=3:
			self.size = args[2]
		else:
			self.size =16
		if len(args)>=4:
			self.anchor = args[3]
		else:
			self.anchor = "center"
		self.font = pg.font.Font(self.filePath+self.file,round(self.size*(game.scale/2)))
		self.img = self.font.render(self.text, True, (0,0,0), (255,255,255))
		self.rect = self.img.get_rect()
		