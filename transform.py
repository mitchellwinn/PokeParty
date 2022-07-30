import numpy as np
import game
import asyncio

class Transform(object):
	#depending on the specificity of the arguments passed, we can
	#initialize transforms lazily, or in great detail
	def __init__(self, *args):
		if len(args)==0:
			self.position = [0,0]
			self.rotation = [0,0]
			self.scale = [2,2]
		elif len(args)==1:
			self.position = args[0]
			self.rotation = [0,0]
			self.scale = [2,2]
		elif len(args)==2:
			self.position = args[0]
			self.rotation = args[1]
			self.scale = [2,2]
		elif len(args)==3:
			self.position = args[0]
			self.rotation = args[1]
			self.scale = args[2]

	def setPos(self, newPos):
		self.position = newPos

	def translate(translation):
		self.position = self.position + translation

	async def moveOverTime(self, newPos,duration):
		elapsedTime = 0
		initialPos = self.position
		distance = game.subNumbers(newPos,initialPos)
		while elapsedTime<duration:
			self.position = game.addNumbers(initialPos,game.scaleList(distance,(elapsedTime/duration)))
			elapsedTime += game.timestep
			await asyncio.sleep(game.timestep*1)
		self.position = newPos

	async def smoothMoveOverTime(self, newPos,duration):
		elapsedTime = 0
		initialPos = self.position
		distance = game.subNumbers(newPos,initialPos)
		while elapsedTime<duration:
			self.position = game.addNumbers(initialPos,game.scaleList(distance,(elapsedTime/duration)**2))
			elapsedTime += game.timestep
			await asyncio.sleep(game.timestep*1)
		self.position = newPos

	async def moveAtSpeed(self, newPos,speed):
		print("Called moveAtSpeed()")
		#we need a numpy array so that we can normalize our distance vector to get direction
		distanceVector = np.array(newPos-self.position)
		direction = distanceVector / np.ndarray.tolist(np.linalg.norm(distanceVector))
		while distance>0.1:
			print("Distance from destination: "+distance)
			self.position = game.addNumbers(self.position,(game.scaleList(direction,game.timestep*speed)))
			distance = math.dist(self.position,newPos)
			#print(game.timestep)
			await asyncio.sleep(game.timestep)
		self.position = newPos

	def sortOrder(self):
		return self.position[1]

    

