import socket
import pickle
import asyncio
import random
import game
import os
import time
from threading import Thread
from gameobject import GameObject, findByName
from sprite import Sprite
from text import Text



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
            if True:
                self.updating = True
                count=1
                for p in game.allPlayers:
                    delete = True
                    for i in msg.strings:
                        if p.getNamedComponent("client").id == i.strings[0]:
                            delete = False
                    if(delete):
                        game.gameObjects.remove(findByName("label"+str(p.getNamedComponent("client").id)))
                        game.gameObjects.remove(findByName("pokemon"+str(p.getNamedComponent("client").id)))
                        game.gameObjects.remove(findByName("ready"+str(p.getNamedComponent("client").id)))
                        game.allPlayers.remove(p)
                for i in msg.strings:
                    if i.strings[0] == self.id:
                        continue
                    exists = False
                    for p in game.allPlayers:
                        if p.getNamedComponent("client").id == i.strings[0]:
                            exists = True
                    if(exists==False):
                        thisPlayer = GameObject(str(i.strings[0]),[game.windowDimensions[0]*.165+game.windowDimensions[0]*count*.2,game.windowDimensions[1]*0.775])
                        thisPlayer.addComponent(Client(self.room),"client")
                        thisPlayer.getNamedComponent("client").id = i.strings[0]
                    else:
                        thisPlayer = findByName(str(i.strings[0]))
                    thisPlayer.getNamedComponent("client").name = i.strings[1]
                    thisPlayer.getNamedComponent("client").trainer = i.strings[2]
                    thisPlayer.getNamedComponent("client").starter = i.strings[3]
                    thisPlayer.getNamedComponent("client").ready = i.strings[4]
                    thisPlayer.getNamedComponent("client").idstarter = game.starterList[i.strings[3]]
                    #Update Room Trainer Pokemon and Label
                    if game.gameState=="inRoom":
                        try:
                            thisPlayer.getNamedComponent("sprite").fileChange(str(thisPlayer.getNamedComponent("client").trainer)+".png")
                        except:
                             thisPlayer.addComponent(Sprite(str(i.strings[2])+".png","trainers\\","png"),"sprite")
                        try:
                            if(i.strings[4]==True):
                                findByName("ready"+str(i.strings[0])).getNamedComponent("ready").fileChange("ready.gif")
                            else:
                                findByName("ready"+str(i.strings[0])).getNamedComponent("waiting").fileChange("ready.gif")
                            findByName("ready"+str(i.strings[0])).getNamedComponent("ready").playing =True
                        except:
                            game.gameObjects.append(GameObject("ready"+str(i.strings[0]),[game.windowDimensions[0]*.21+game.windowDimensions[0]*count*.2,game.windowDimensions[1]*(0.895-((count)%2)*.05)]))
                            findByName("ready"+str(i.strings[0])).addComponent(Sprite("waiting.gif","","gif"),"sprite")
                        try:
                            findByName("label"+str(i.strings[0])).getNamedComponent("text").text = str(i.strings[1])
                        except:
                            game.gameObjects.append(GameObject("label"+str(i.strings[0]),[game.windowDimensions[0]*.165+game.windowDimensions[0]*count*.2,game.windowDimensions[1]*(0.5+((count)%2)*.05)]))
                            findByName("label"+str(i.strings[0])).addComponent(Text(i.strings[1],"pokemon1.ttf"),"text")
                        try:
                            findByName("pokemon"+str(i.strings[0])).getNamedComponent("sprite").fileChange(str(thisPlayer.getNamedComponent("client").starter)+".png")
                        except:
                            game.gameObjects.append(GameObject("pokemon"+str(i.strings[0]),[game.windowDimensions[0]*.255+game.windowDimensions[0]*count*.2,game.windowDimensions[1]*0.855]))
                            findByName("pokemon"+str(i.strings[0])).addComponent(Sprite(str(i.strings[3])+".png","pokemon\\","png"),"sprite")
                    count+=1
                    newAllPlayers.append(thisPlayer)
                    count+=1
                count =1
                    
            game.allPlayers = newAllPlayers
            self.updating = False




    def send(self, data, wait):
        time1 = time.time()
        try:
            #send desired communication to server
            self.client.send(data)
            if wait==False:
                return -1
            print(f"Sent data to server!\nWaiting on response...!")
            #get desired communication from server
            try:
                reply = self.client.recv(self.header)
            except:
                return -1
            print(f"Got response from server!")
            reply = pickle.loads(reply)
            print(f"Purpose: {reply.purpose}")
            #interpret the reply and do something client sided in response
            self.serverMsgInterpret(reply)
        except socket.error as e:
            print(f"[SOCKET ERROR]: {e}")
            return -1
        time2 = time.time()
        deltaTime = time2 - time1
        return deltaTime

    def __init__(self, room):
        self.connected = "UNDECIDED"
        self.ready=False
        self.name = os.getlogin( )[0:os.getlogin( ).find(" ")]
        self.header = 2048
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


