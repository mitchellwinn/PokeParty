import pygame as pg

class Sprite(object):

	def __init__(self,*args):
		self.filePath = "sprites\\"+args[1]
		self.file=args[0]
		self.img = pg.image.load(self.filePath+self.file)

	def fileChange(self, file):
		self.file=file
		self.img = pg.image.load(self.filePath+self.file)