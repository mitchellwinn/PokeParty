import socket
import pickle
import asyncio
import game
import os
from threading import Thread



class SimpleData(object):
    def __init__(self, purpose, strings):
        self.purpose = purpose
        self.strings = strings

    def getAsDataString(self):
        dataString = pickle.dumps(self)
        return dataString

    def toString(self):
        data = f"SimpleData:{self.purpose}:"
        for i in self.strings:
            data+= f"\n{str(i)}"
        return data


class Client(object):

    def serverMsgInterpret(self, msg):
        if msg.purpose == self.DISCONNECT_MESSAGE:
            game.gameObjects.clear()
            game.gameState = "title"
            del(self)
        elif msg.purpose == "SETROOM":
            self.room = msg.strings[0]
            print("updated room!")
        elif msg.purpose == "GETUPDATES":
            #we don't need to do anything with an update about ourselves, as thats information we originally gave out, and this is client authoritative since its a boardgame
            game.allPlayers.clear()
            for i in msg.strings:
                if i.strings[0] == self.id:
                    continue
                game.allPlayers.append(i)

    def send(self, data, wait):
        try:
            #send desired communication to server
            self.client.send(data)
            if wait==False:
                return
            print(f"Sent data to server!\nWaiting on response...!")
            #get desired communication from server
            reply = self.client.recv(self.header)
            print(f"Got response from server!")
            reply = pickle.loads(reply)
            print(f"Purpose: {reply.purpose}")
            #interpret the reply and do something client sided in response
            self.serverMsgInterpret(reply)
        except socket.error as e:
            print(f"[SOCKET ERROR]: {e}")
            return -1

    def __init__(self, room):
        self.connected = "UNDECIDED"
        self.name = print(os.getlogin( )[0:os.getlogin( ).find(" ")])
        self.header = 4096
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '173.255.244.44'
        self.port = 1234
        self.addr = (self.host, self.port)
        self.ADDRESS = ""
        self.desiredRoom = room
        self.DISCONNECT_MESSAGE = "!DISCONNECT"

    def getAsDataString(self, purpose):
        self.purpose = purpose
        self.associatedObject = game.playerObject
        dataString = pickle.dumps(self)
        print(data)
        return dataString

    def connect(self):
        try:
            self.id =  self.client.connect(self.addr)
        except:
            print("connection unsuccessful")
            self.connected = "FAILURE"
            return
        print("connection successful")
        self.connected = "SUCCESS"
        reply = self.client.recv(self.header)
        print(f"Got response from server!")
        reply = pickle.loads(reply)
        self.id = reply.strings[0]
        toSend = SimpleData("ROOM",[self.desiredRoom,self.id,self.name])
        self.send (toSend.getAsDataString(),True)
        toSend = SimpleData("GETUPDATES",[self.room])
        self.send (toSend.getAsDataString(),True)
