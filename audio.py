import pygame as pg
import asyncio
import game

global filepath
filepath = "sounds\\"

def playSound(soundName):
	sound = pg.mixer.Sound(filepath+soundName)
	sound.set_volume(game.volume*.75)
	pg.mixer.Sound.play(sound)

def playMusic(musicName):
	pg.mixer.music.load(filepath+musicName)
	pg.mixer.music.set_volume(game.volume*1)
	pg.mixer.music.play(-1)

def stopMusic():
	pg.mixer.music.stop()