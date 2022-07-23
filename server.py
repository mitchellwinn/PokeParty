import socket
import pickle
import asyncio
import aioconsole
from room import Room
from gameobject import GameObject
from client import SimpleData
import pygame as pg

async def startServer():
	pg.init()
	asyncio.create_task(listenForInput())
	global rooms, DISCONNECT_MESSAGE, s
	rooms = []
	HEADER = 4096
	SERVER = ''
	PORT = 1234
	DISCONNECT_MESSAGE = "!DISCONNECT"
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.bind((SERVER, PORT))
	except socket.error as e:
		print(f"[SOCKET ERROR]: {e}")
	s.listen()
	while True:
		conn, addr = s.accept()
		asyncio.create_task(handleClient(conn, addr))
		clients = 0
		count = 0
		for i in asyncio.Task.all_tasks():
			if(i.done()):
				return
			count+=1
		clientCount = count
		print(f"[ACTIVE CONNECTIONS]{clientCount}")

#send a message to the associated client via their asynchronous handling process
def send(conn,data):
	try:
		s.send(data)
	except socket.error as e:
		print(f"[SOCKET ERROR]: {e}")

#send a message to all clients aside from the associate client address (for updating other clients on things)


def clientMsgInterpret(conn, addr, msg):
	connected = True
	#-----
	#-----disconnect client from server
	if msg.purpose == DISCONNECT_MESSAGE:
		#remove player association from the room
		for i in rooms:
			for k in i.players:
				if k == msg.id:
					i.players.remove(k)
		response = SimpleData("!DISCONNECT",[])
		send(conn, response.getAsDataStringInput())
		connected = False
	#-----
	#-----check room status before player is allowed to join
	elif msg.purpose=="ROOM":
		roomAlreadyExists = False
		for i in rooms:
			if i.name == msg.desiredRoom:
				thisRoom = i
				roomAlreadyExists = True
		if roomAlreadyExists == False:
			thisRoom = Room(msg.desiredRoom)
			msg.room = msg.desiredRoom
			thisRoom.players.append(msg.associatedObject)
			rooms.append(thisRoom)
		else:
			msg.room = msg.desiredRoom
			thisRoom.players.append(msg)
		response = SimpleData("SETROOM",["msg.desiredRoom"])
		send(conn ,response.getAsDataStringInput())
	#-----
	#-----updates server's knowledge of a specific player in a room
	elif msg.purpose=="UPDATE":
		for i in rooms:
			if i.name == msg.room:
				for k in i.players:
					if k.id == msg.id:
						k = msg
	#-----
	#-----updates clients knowledge of all players in a room
	elif msg.purpose=="GETUPDATES":
		for i in rooms:
			if i.name == msg.room:
				dataString = pickle.dumps(i.players)
				send(conn ,dataString)
	return connected

async def handleClient(conn, addr):
	print(f"[NEW CONNECTION] client:{addr} connected!") 
	connected = True
	while connected:
		data = conn.recv(HEADER)
		data = pickle.loads(data)
		connected = clientMsgInterpret(conn, addr, data)
		try:
			print(f"client:{addr} sent message with purpose:{data.purpose}")
		except:
			asyncio.sleep(0)
	conn.close()

async def listenForInput():
	print("ESC to stop server")
	while(True):
		events = pg.event.get()
		for event in events:
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					quit()

asyncio.run(startServer())