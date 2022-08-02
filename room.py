import game

class Room(object):
	def __init__(self,*args):
		self.name =args[0]
		self.players = []
		self.started = False