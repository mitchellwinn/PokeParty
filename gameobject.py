import game
import transform
from sprite import Sprite

class GameObject(object):

	def __init__(self,*args):
		self.components = []
		self.index = len(game.gameObjects)
		if len(args)==0:
			self.name = "Unnamed"
			self.transform = transform.Transform()
		elif len(args)==1:
			self.name = args[0]
			self.transform = transform.Transform()
		elif len(args)==2:
			self.name = args[0]
			self.transform = transform.Transform(args[1])
		elif len(args)==3:
			self.name = args[0]
			self.transform = transform.Transform(args[1],args[2])
		elif len(args)==4:
			self.name = args[0]
			self.transform = transform.Transform(args[1],args[2],args[3])
		#print("new GameObject "+self.name+" initialized at:\n"+str(self.transform.position))
		self.networkID=-1

	def addComponent(self, component, name):
		self.components.append([component,name]);
		game.frame = 0
		game.updateDisplay()

	def removeComponent(self, name):
		for i in self.components:
			if i[1]==name:
				self.components.remove(i);
		game.frame = 0
		game.updateDisplay()

	def getNamedComponent(self, name):
		for i in self.components:
			if i[1]==name:
				return i[0]
		return -1

	def destroy(self):
		game.gameObjects.remove(self)
		print("GameObject "+self.name+" is no longer being used")

def findByName(named):
		for i in game.gameObjects:
			if(i.name==named):
				return i

