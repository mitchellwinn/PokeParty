listt = [1,2,3,4]

class Bob(object):
	def __init__(self,*args):
		print(len(listt))
		self.name = "ob"


#bob = bob()
listt.append(Bob())
print(len(listt))
