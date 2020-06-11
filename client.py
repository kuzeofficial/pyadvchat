#! /usr/bin/env python
#! -*- coding: utf-8 -*-

# Client TCP Chat
#Author = Cristian Fonseca Comas
#Age = 16
#Date = may 3 of 2019
#A.K.A = Kuze

#This is a client chat used sockets

#Import library
import socket, select, string, sys
# Console colors
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan
GR = '\033[37m' # gray
T  = '\033[93m' # tan

#Create de prompt and recursive mode
def prompt() :
	sys.stdout.write(str(T+'You>> '+W))
	sys.stdout.flush()

#main function
if __name__ == "__main__":
	if(len(sys.argv) < 3) :
		print('Usage : python client.py hostname port')
		sys.exit()
	#Variable declaration
	host = sys.argv[1]
	port = int(sys.argv[2])
	#Create de socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)
	
	# connect to remote host
	try :
		s.connect((host, port))
		print(G+'[INFO] Connected to remote host'+W)
		username = str(input('Write your user name: '))
		if username == "":
			username = "anonimous"
	except :
		print(R+'[ERROR] Unable to connect'+W)
		sys.exit()
	
	prompt()
	
	while 1:
		socket_list = [sys.stdin, s]
		
		# Get the list sockets which are readable
		try:
			read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
		except:
			sys.exit()
		for sock in read_sockets:
			#incoming message from remote server
			if sock == s:
				data = sock.recv(4096)
				if not data :
					print(R+'\nDisconnected from chat server\n'+W)
					sys.exit()
				else :
					#print data(msj)
					sys.stdout.write(data)
					prompt()
			
			#user entered a message
			else :
				try:
					msg = sys.stdin.readline()
					s.send(((G+username+W)+(R+'>>'+W)+' '+ msg))
					prompt()
				except KeyboardInterrupt:
					print('\nDisconnected from chat server')
					sys.exit()
