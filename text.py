import pygame as pg
import asyncio

class Text(object):

	def __init__(self,*args):
		self.filePath = "fonts\\"
		self.file=args[1]
		self.text=args[0]