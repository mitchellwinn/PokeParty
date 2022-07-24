import socket
import pickle
import asyncio
from room import Room
from gameobject import GameObject
from client import SimpleData
import pygame as pg

async def startServer():
	try:
		pg.init()
		print("Pygame initizlized")
	except:
		print("Failed to initialize Pygame")
		quit()
	global rooms, DISCONNECT_MESSAGE, s, HEADER
	rooms = []
	HEADER = 4096
	SERVER = ''
	PORT = 1234
	TIMEOUT=3
	DISCONNECT_MESSAGE = "!DISCONNECT"
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(TIMEOUT)
	s.setblocking(False)
	try:
		s.bind((SERVER, PORT))
		print(f"Successfully bound socket server to {SERVER}:{PORT}")
	except socket.error as e:
		print(f"[SOCKET ERROR]: {e}")
	s.listen()
	asyncio.create_task(lfi())
	await asyncio.sleep(0)
	print("Awaiting connection from next client...")
	while True:		
		try:
			conn, addr = s.accept()
		except:
			continue
		asyncio.create_task(handleClient(conn, addr))
		clients = 0
		count = 0
		for i in asyncio.Task.all_tasks():
			if(i.done()):
				return
			count+=1
		clientCount = count
		print(f"[ACTIVE CONNECTIONS]{clientCount}")
		print("Awaiting connection from next client...")
		await asyncio.sleep(0)

#send a message to the associated client via their asynchronous handling process
def send(conn,data):
	try:
		conn.send(data)
	except socket.error as e:
		print(f"[SOCKET ERROR]: {e}")

#send a message to all clients aside from the associate client address (for updating other clients on things)


def clientMsgInterpret(conn, addr, msg):
	try:
		print(f"The message's purpose: {msg.purpose}")
	except:
		return True
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
	global HEADER
	print(f"[NEW CONNECTION] client:{addr} connected!") 
	connected = True
	conn.settimeout(3)
	conn.setblocking(False)
	while connected:
		try:
			data = conn.recv(HEADER)
		except:
			break
		data = pickle.loads(data)
		connected = clientMsgInterpret(conn, addr, data)
		try:
			print(f"client:{addr} sent message with purpose:{data.purpose}")
		except:
			asyncio.sleep(0)
		await asyncio.sleep(0)
	conn.close()

async def lfi():
	print("CRTL+C to halt program")

asyncio.run(startServer())