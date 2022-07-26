import socket
import pickle
import asyncio
import game

class SimpleData(object):
    def _init_(self, purpose, strings):
        self.purpose = purpose
        self.strings = []

    def getAsDataString(self):
        dataString = pickle.dumps(self)
        return dataString


class Client(object):

    def __init__(self, room):
        self.connected = "UNDECIDED"
        self.header = 4096
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.client.settimeout(3)
        self.host = '173.255.244.44'
        self.port = 1234
        self.addr = (self.host, self.port)
        self.id = self.connect()
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
            self.client.connect(self.addr)
        except:
            print("connection unsuccessful")
            self.connected = "FAILURE"
        print("connection unsuccessful")
        self.connected = "SUCCESS"
        send (self.getAsDataString("ROOM"))
        send (self.getAsDataString("GETUPDATES"))


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

    def serverMsgInterpret(self, msg):
        connected = True
        if msg.stirngs[0] == self.DISCONNECT_MESSAGE:
            connected = False
        elif msg.purpose == "SETROOM":
            self.room = msg.strings[0]
        elif msg[0].purpose == "GETUPDATES":
            #we don't need to do anything with an update about ourselves, as thats information we originally gave out, and this is client authoritative since its a boardgame
            for i in game.otherPlayers:
                i.removeFromClient = True
                for thisMsg in msg:
                    if thisMsg.id == self.id:
                        return
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

        return connected
