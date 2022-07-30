import socket
import pickle
import asyncio
import random
import game
import os
import time
from threading import Thread
from gameobject import GameObject
from sprite import Sprite



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
            newAllPlayers=[]
            try:
                game.gameObjects.remove(findByName("label"+str(self.id)))
                game.gameObjects.remove(findByName("pokemon"+str(self.id)))
            except:
                print("")
            if True:
                count=1
                for i in msg.strings:
                    if i.strings[0] == self.id:
                        continue
                    game.gameObjects.append(GameObject("label"+str(self.id),[game.windowDimensions[0]*.165+game.windowDimensions[0]*count*.2,game.windowDimensions[1]*0.5]))
                    findByName("label"+str(self.id)).addComponent(Text(self.name,"pokemon1.ttf"),"text")
                    thisPlayer = GameObject(str(i.strings[0]),[game.windowDimensions[0]*.165+game.windowDimensions[0]*count*.2,game.windowDimensions[1]*0.775])
                    thisPlayer.addComponent(Client(self.room),"client")
                    thisPlayer.getNamedComponent("client").id = i.strings[0]
                    thisPlayer.getNamedComponent("client").name = i.strings[1]
                    thisPlayer.getNamedComponent("client").trainer = i.strings[2]
                    thisPlayer.getNamedComponent("client").starter = i.strings[3]
                    if game.gameState=="inRoom":
                        thisPlayer.addComponent(Sprite(str(thisPlayer.getNamedComponent("client").trainer)+".png","trainers\\","png"),"sprite")
                    newAllPlayers.append(thisPlayer)
                    count+=1
                for i in msg.strings:
                    if i.strings[0] == self.id:
                        continue
                    game.gameObjects.append(GameObject("pokemon"+str(self.id),[game.windowDimensions[0]*.195+game.windowDimensions[0]*count*.2,game.windowDimensions[1]*0.8]))
                    findByName("pokemon"+str(self.id)).addComponent(Sprite(str(thisPlayer.getNamedComponent("client").starter)+".png","pokemon\\","png"),"sprite")
            game.allPlayers = newAllPlayers




    def send(self, data, wait):
        try:
            #send desired communication to server
            self.client.send(data)
            if wait==False:
                return
            print(f"Sent data to server!\nWaiting on response...!")
            #get desired communication from server
            try:
                reply = self.client.recv(self.header)
            except:
                print(f"[SOCKET ERROR]: {e}")
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
        self.name = os.getlogin( )[0:os.getlogin( ).find(" ")]
        self.header = 4096
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '173.255.244.44'
        self.port = 1234
        self.addr = (self.host, self.port)
        self.ADDRESS = ""
        self.desiredRoom = room
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        #self.trainer = random.randint(1,34)

    def getAsDataString(self, purpose):
        self.purpose = purpose
        self.associatedObject = game.playerObject
        dataString = pickle.dumps(self)
        print(data)
        return dataString

    def getUpdates(self):
        print("hi")
        while True:
            time.sleep(.75)
            toSend = SimpleData("GETUPDATES",[self.room])
            try:
                self.send (toSend.getAsDataString(),True)
            except socket.error as e:
                print(f"[SOCKET ERROR]: {e}")


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
        toSend = SimpleData("ROOM",[self.desiredRoom,self.id,self.name,self.trainer,self.starter])
        self.send (toSend.getAsDataString(),True)
        toSend = SimpleData("GETUPDATES",[self.room])
        self.send (toSend.getAsDataString(),True)
        thread = Thread(target=self.getUpdates)
        thread.start()


