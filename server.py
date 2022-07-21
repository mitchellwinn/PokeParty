import socket

def startServer():
	global playerUIDs, server, port
	server = 
	port = 1234
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((server), port)
	s.listen