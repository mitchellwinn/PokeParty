import socket
import pickle
import asyncio
import game
from threading import Thread



class SimpleData(object):
    def __init__(self, purpose, strings):
        self.purpose = purpose
        self.strings = []

    def getAsDataString(self):
        dataString = pickle.dumps(self)
        return dataString


class Client(object):

    def serverMsgInterpret(self):
        msg = reply
        if msg.purpose == self.DISCONNECT_MESSAGE:
            game.gameObjects.clear()
            game.gameState = "title"
            del(self)
        elif msg.purpose == "SETROOM":
            self.room = msg.strings[0]
            print("updated room!")
        elif msg[0].purpose == "GETUPDATES":
            #we don't need to do anything with an update about ourselves, as thats information we originally gave out, and this is client authoritative since its a boardgame
            for i in game.otherPlayers:
                i.removeFromClient = True
                for thisMsg in msg:
                    if thisMsg.id == self.id:
                        continue
                    referenceExists = False
                    if i.id == thisMsg.id:
                        referenceExists = True
                        i.removeFromClient = False
                        i = thisMsg
                    elif referenceExists == False:
                        game.otherPlayers.append(msg)
                if(i.removeFromClient):
                    game.otherPlayers.remove(i)
            game.allPlayersInRoom = game.otherPlayers
            game.allPlayersInRoom.append(game.playerObject)

    def send(self, data):
        try:
            #send desired communication to server
            self.client.send(data)
            #get desired communication from server
            reply = self.client.recv(self.header)
            reply = pickle.loads(reply)
            #interpret the reply and do something client sided in response
            serverMsgInterpret(reply)
            return reply
        except socket.error as e:
            print(f"[SOCKET ERROR]: {e}")
            return -1

    def __init__(self, room):
        self.connected = "UNDECIDED"
        self.header = 4096
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.client.settimeout(3)
        self.host = '173.255.244.44'
        self.port = 1234
        self.addr = (self.host, self.port)
        self.desiredRoom = room
        self.connect()
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

        #self.serverHandler()
        self.send (SimpleData("ROOM",[self.desiredRoom,self.id]).getAsDataString())
