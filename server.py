import socket
import pickle
from room import Room
from gameobject import GameObject
from client import SimpleData, Client
from threading import Thread

def startServer():
	global rooms, DISCONNECT_MESSAGE, s, HEADER
	rooms = []
	HEADER = 4096
	SERVER = ''
	PORT = 1234
	DISCONNECT_MESSAGE = "!DISCONNECT"
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.bind((SERVER, PORT))
		print(f"Successfully bound socket server to {SERVER}:{PORT}")
	except socket.error as e:
		print(f"[SOCKET ERROR]: {e}")
	s.listen()
	print("CRTL+C to halt program")
	print("Awaiting connection from next client...")
	while True:		
		conn, addr = s.accept()
		thread = Thread(target=handleClient,args=(conn, addr))
		thread.start()
		clients = 0
		count = 0
		print("Awaiting connection from next client...")

#send a message to the associated client via their asynchronous handling process
def send(conn,data):
	try:
		conn.send(data)
	except socket.error as e:
		print(f"[SOCKET ERROR]: {e}")

#send a message to all clients aside from the associate client address (for updating other clients on things)


def clientMsgInterpret(conn, addr, msg):
	try:
		print(f"Client:{addr} message's purpose: {msg.purpose}")
	except:
		return True
	connected = True
	#-----
	#-----disconnect client from server
	if msg.purpose == DISCONNECT_MESSAGE:
		#remove player association from the room
		for i in rooms:
			for k in i.players:
				if k.id == msg.strings[0]:
					i.players.remove(k)
			if len(i.players)==0:
				rooms.remove(i)
		connected = False
	#-----
	#-----check room status before player is allowed to join
	elif msg.purpose=="ROOM":
		print(f"Checking to see if room already exists...")
		roomAlreadyExists = False
		for i in rooms:
			if i.name == msg.strings[0]:
				thisRoom = i
				print(f"The requested room {msg.strings[0]} already exists...")
				roomAlreadyExists = True
		if roomAlreadyExists == False:
			try:
				print(f"The requested room {msg.strings[0]} does not yet exist...")
			except:
				print("error with msg.strings")
			try:
				thisRoom = Room(msg.strings[0])
				thisClient = Client(msg.strings[0])
			except:
				print("could not make Room/Client server instance!")
				response = SimpleData("!DISCONNECT",[msg.strings[0]])
				send(conn ,response.getAsDataString())
				return connected
			thisClient.id = msg.strings[1]
			thisClient.name = msg.strings[2]
			thisClient.trainer = msg.strings[3]
			thisClient.starter = msg.strings[4]
			thisRoom.players.append(thisClient)
			rooms.append(thisRoom)
			print(f"Adding client:{msg.strings[1]} to NEW room {msg.strings[0]}!")
		else:
			thisClient = Client(msg.strings[0])
			thisClient.id = msg.strings[1]
			thisClient.name = msg.strings[2]
			thisClient.trainer = msg.strings[3]
			thisClient.starter = msg.strings[4]
			thisRoom.players.append(thisClient)
			print(f"Adding client:{msg.strings[1]} to EXISTING room {msg.strings[0]}!")
			print(f"EXISTING room {msg.strings[0]} now has {len(thisRoom.players)} players!")
		response = SimpleData("SETROOM",[msg.strings[0]])
		send(conn ,response.getAsDataString())
	#-----
	#-----updates server's knowledge of a specific player in a room
	elif msg.purpose=="UPDATE":
		for i in rooms:
			if i.name == msg.room:
				for k in i.players:
					print("")					
	#-----
	#-----updates clients knowledge of all players in a room
	elif msg.purpose=="GETUPDATES":
		players = []
		for i in rooms:
			if i.name == msg.strings[0]:
				for k in i.players:
					players.append(SimpleData("ONLINEPLAYER",[k.id,k.name,k.trainer,k.starter]))
				response = SimpleData("GETUPDATES",players)
				try:
					send(conn ,response.getAsDataString())
				except socket.error as e:
					print(f"failed to send a response... error:{e}")
					response = SimpleData("!DISCONNECT",[""])
					try:
						send(conn ,response.getAsDataString())
					except:
						print(f"failed to send a disconnect message... error:{e}")
	#-----
	#-----
	return connected

def handleClient(conn, addr):
	global HEADER
	print(f"[NEW CONNECTION] Client:{addr} connected!") 
	connected = True
	response = SimpleData("SETID",[addr])
	send(conn ,response.getAsDataString())
	while connected:
		print(f"Client:{addr} receiving data...")
		data = conn.recv(HEADER)
		try:
			try:
				data = pickle.loads(data)
			except:
				print(f"Client:{addr} sent data that could not be unpacked by pickled.loads(data)")
			connected = clientMsgInterpret(conn, addr, data)
		except socket.error as e:
			print(f"Client:{addr} sent data that the server could not respond to. error:{e}")
			continue
	conn.close()

startServer()